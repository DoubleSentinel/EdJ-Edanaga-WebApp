from flask import Flask, render_template, redirect, url_for, abort, request

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_security import Security, MongoEngineUserDatastore

from flask_admin import Admin, helpers

app = Flask(__name__)

@app.route("/")
def home():
    return "This is the admin interface"
