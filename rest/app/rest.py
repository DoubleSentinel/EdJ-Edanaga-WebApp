import datetime
from flask import Flask, request, jsonify

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_mongorest import MongoRest, methods
from flask_mongorest.views import ResourceView

from models import TestUser, Invitations, ObjectiveName

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


@api.register(name='is_user', url='/is_user/')
class IsUserView(ResourceView):
    resource = IsUserResource
    methods = [methods.List]


@app.route("/login_user/", methods=['POST'])
def login():
    try:
        user = TestUser.objects.get(username=request.json["username"])
        if user.userpass == request.json["userpass"]:
            user.last_login = datetime.datetime.utcnow()
            out = []
            for variable in Invitations.objects.get(participants=user.id).constant_variables.variable_set:
                out.append({"name": variable.name.unity_name,
                            "description": variable.description,
                            "unit": variable.unit,
                            "worst": variable.worst,
                            "best": variable.best,
                            "global_weight": variable.global_weight,
                            })
            return jsonify(error={"code": 200, "message": "ok", "constants": out})
        else:
            return jsonify(error={"code": 400, "message": "wrong password"})
    except KeyError:
        return jsonify(error={"code": 400, "message": "Bad request"})
    except mongoerrors.DoesNotExist:
        return jsonify(error={"code": 400, "message": "Username does not exist"})


@app.route("/update_invite/", methods=['POST'])
def update_invite():
    try:
        token = Invitations.objects.get(token_url=request.json["token_url"])
        token.update(add_to_set__participants=request.json["user_id"])
        return jsonify(error={"code": 200, "message": "ok", "id": str(token.id)})
    except KeyError:
        return jsonify(error={"code": 400, "message": "Bad request"})
    except mongoerrors.DoesNotExist:
        return jsonify(error={"code": 400, "message": "Token does not exist"})
