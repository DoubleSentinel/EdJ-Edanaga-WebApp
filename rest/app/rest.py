from flask import Flask, render_template, redirect, url_for, abort, request

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_restx import Api, Resource, fields

app = Flask(__name__)

@app.route("/")
def home():
    return "This is the api interface"

