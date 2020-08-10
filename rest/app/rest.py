from flask import Flask, request, jsonify

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_mongorest import MongoRest, methods
from flask_mongorest.views import ResourceView

from models import TestUser

from resources import (LanguagesResource,
                       SceneResource,
                       UITranslationsResource,
                       TestUserResource,
                       IsUserResource)

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)

# Flask MongoRest init
api = MongoRest(app)


@api.register(name='languages', url='/languages/')
class LanguageView(ResourceView):
    resource = LanguagesResource
    methods = [methods.List]


@api.register(name='scenes', url='/scenes/')
class SceneView(ResourceView):
    resource = SceneResource
    methods = [methods.Fetch, methods.List]


@api.register(name='ui', url='/ui/')
class UITranslationsView(ResourceView):
    resource = UITranslationsResource
    methods = [methods.Fetch, methods.List]


@api.register(name='crud_user', url='/crud_user/')
class TestUserView(ResourceView):
    resource = TestUserResource
    methods = [methods.Create, methods.Update]


@api.register(name='isuser', url='/is_user/')
class IsUserView(ResourceView):
    resource = IsUserResource
    methods = [methods.List]


@app.route("/login_user/", methods=['POST'])
def login():
    try:
        if TestUser.objects.get(username=request.json["username"]).userpass == request.json["userpass"]:
            return jsonify(error={"code": 200, "message": "ok"})
        else:
            return jsonify(error={"code": 400, "message": "wrong password"})
    except KeyError:
        return jsonify(error={"code": 400, "message": "Bad request"})
    except mongoerrors.DoesNotExist:
        return jsonify(error={"code": 400, "message": "Username does not exist"})

