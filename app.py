import os, csv, hashlib, magic
from datetime import date, datetime
import db

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def on_start():
    #create csv and add header
    cwd = os.getcwd() # root directory of this python file
    sourcedir = cwd + "/static/images_go_here/" # directory for source images

    # set up prefix and suffix
    global prefix
    prefix = ""
    global suffix
    suffix = ""

    # format filename with unique id and current date
    today = date.today()
    global session_id
    session_id = str(db.next_csv_id())

    global csv_filename
    csv_filename = cwd + "/imagetags" + session_id + "_" + str(today.strftime("%Y_%m_%d")) + ".csv" # output csv filename    
    #print("csv_filename:", csv_filename)
    # open csv file
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # write header
        writer.writerow(['id', 'count', 'filename', 'md5hash', 'filetype', 'tagged_date', 'data'])
        
    # add image files to db
    # TODO: handle no images
    img_count = 0
    for path, dirs, files in os.walk(sourcedir):
        for filename in files:
            print("filename:", filename)

            # hash file
            hasher = hashlib.md5() # put file in buffer to get hash
            with open(str(sourcedir + filename), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            print(hasher.hexdigest())

            # get filetype
            filetype = magic.from_file(str(sourcedir + filename))
            #filetype = "todo"

            # write filename and hash to csv row
            #writer.writerow([img_count, filename, hasher.hexdigest(), filetype])
                    
            # iterate image count
            img_count = img_count + 1

            # add id, session_id, filename, hash, filetype to db
            db.addimage(session_id, img_count, filename, hasher.hexdigest(), filetype)

    # save total image count
    global img_total
    img_total = img_count

# main page with summary
@app.route("/", methods=["GET", "POST"])
def index():
    global prefix
    global suffix
    if request.method == "POST":
        # save prefix/suffix
        prefix = request.form.get("prefix")
        suffix = request.form.get("suffix")

        # combine prefix, data and suffix
        tag_data = prefix + request.form.get("data") + suffix
        # add tag data to db
        db.add_tag(session["img_id"], tag_data)

        # add all data to csv file
        img_filename, img_count, image_filetype, image_hash = db.get_image_data(session["img_id"])

        with open(csv_filename, 'a') as f:
            # write image data
            writer = csv.writer(f)
            writer.writerow([session["img_id"], img_count, img_filename, image_hash, image_filetype, datetime.now(), tag_data])

        # redirect
        return redirect("/")
    else:
        # get next untagged image. TODO: display message if no more untagged images.  get total count and current image count
        
        # get next image data from db
        img_id, img_filename, img_count, image_filetype, image_hash = db.get_next_image(session_id)
        
        # save image id
        session["img_id"] = img_id

        # combine image count and total for display
        image_count = str(img_count) + "/" + str(img_total)
        
        # put together path for image
        image_path = "/static/images_go_here/" + img_filename # TODO: figure out how to have flask call images_go_here folder 

        return render_template("index.html", image_count=image_count, image_path=image_path, image_name=img_filename, image_filetype=image_filetype, image_hash=image_hash, prefix=prefix, suffix=suffix)

# start flask on running app.py, run on_start
on_start()
app.run(port=8080, host="localhost")