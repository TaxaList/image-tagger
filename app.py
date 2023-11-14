import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

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

# Configure session to use filesystem (not cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# main page
@app.route("/")
def index():
    if request.method == "POST":
        title="tako"
        image = "/tako.jpg"
        return render_template("index.html", title=title, image=image)
    else:
        title="tako"
        image = "/tako.jpg"
        return render_template("index.html", title=title, image=image)

# settings page
@app.route("/settings")
def settings():
    if request.method == "POST":
        header = "test"
        return render_template("history.html", header=header)
    else:
        header = "test"
        return render_template("history.html", header=header)
