import os
from flask import Flask, render_template, redirect, url_for, abort, request, send_from_directory

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from models import Languages, Invitations, HomeScreen

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)


@app.route("/<language>/")
@app.route("/", defaults={'language': 'EN'})
def home(language):
    try:
        content = HomeScreen.objects.get(language=Languages.objects.get(name=language.upper()))
        language_redirects = {language.name: url_for('.home', language=language.name)
                              for language in Languages.objects()}

        return render_template(
            "home.html",
            welcome_title=content.welcome_title,
            welcome_text=content.welcome_text,
            language_redirects=language_redirects,
        )
    except mongoerrors.DoesNotExist:
        token = language
        language_redirects = {language.name: url_for('.unity', language=language.name, token=token)
                              for language in Languages.objects()}
        return render_template(
            "home.html",
            error=f"""The requested language translation of the website isn't available. 
            If you were trying to access a test room make sure you select a language
            in the top right of the page.""",
            language_redirects=language_redirects,
        )


@app.route("/<language>/<token>")
def unity(language, token):
    if not token:
        redirect(url_for('.home', language))
    else:
        try:
            if Invitations.objects.get(token_url=token).active:
                return render_template('unity.html')
            else:
                raise mongoerrors.DoesNotExist
        except mongoerrors.DoesNotExist:
            return render_template(
                "home.html",
                error="It seems your invitation link is either expired, inactive, or erroneous."
            )
