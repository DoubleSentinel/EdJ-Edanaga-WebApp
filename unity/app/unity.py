import os
from flask import Flask, render_template, redirect, url_for, abort, request, send_from_directory

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

#from models import Invitations

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)


@app.route("/<language>")
@app.route("/", defaults={'language': 'en'})
def home(language):
    return render_template(
        "home.html",
        welcome_title="Welcome to Edanaga",
        welcome_text="Filler text"
    )