from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_mongorest import MongoRest, operators, methods
from flask_mongorest.views import ResourceView

from resources import SceneResource, UITextResource

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)

# Flask MongoRest init
api = MongoRest(app)


@api.register(name='scenes', url='/scenes/')
class SceneView(ResourceView):
    resource = SceneResource
    methods = [methods.Fetch, methods.List]


@api.register(name='uitext', url='/ui/')
class UIView(ResourceView):
    resource = UITextResource
    methods = [methods.Fetch, methods.List]
