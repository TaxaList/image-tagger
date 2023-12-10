import os, csv, hashlib, magic
from datetime import date
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

# main page with summary
@app.route("/")
def index():
    
    #create csv and add images to it and db
    cwd = os.getcwd() # root directory of this python file
    sourcedir = cwd + "/static/images_go_here/" # directory for source images

    # format filename with unique id and current date
    today = date.today()
    csv_filename = cwd + "/imagetags" + str(db.next_csv_id()) + "_" + str(today.strftime("%Y_%m_%d")) + ".csv" # output csv filename    
    print("csv_filename:", csv_filename)
    # open csv file
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # write header
        writer.writerow(['id','filename', 'md5hash', 'filetype', 'tagged', 'data', 'tagged_date' ])
        
        # write filenames, hash, filetype
        id = 0
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
                writer.writerow([id, filename, hasher.hexdigest(), filetype])
                id = id + 1

    if request.method == "POST":
        # save prefix/suffix
        # add tag data to db, csv
        # tag last image as "done"
        print("placeholder")
    else:
        # get next untagged image. display message if no more untagged images.get total count and current image count

        image_count = "5/123"
        #cwd = os.getcwd()
        image_name = "tako.jpg"
        image_path = "/static/images_go_here/" + image_name # TODO: figure out how to have flask call images_go_here folder 

        # determine filetype, hash
        image_filetype = "filetypePlaceholderTODO"
        image_hash = "hashPlaceholderTODO"

        # load previous prefix/suffix
        prefix ="testprefixTODO"
        suffix ="testsuffixTODO"

        return render_template("index.html", image_count=image_count, image_path=image_path, image_name=image_name, image_filetype=image_filetype, image_hash=image_hash, prefix=prefix, suffix=suffix)