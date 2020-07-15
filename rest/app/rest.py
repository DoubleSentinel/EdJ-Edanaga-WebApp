from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_mongorest import MongoRest, methods
from flask_mongorest.views import ResourceView

from flask_cors import CORS, cross_origin

from resources import SceneResource, UITranslationsResource

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)

# Flask MongoRest init
api = MongoRest(app)

# Flask CORS init
cors = CORS(app)


@api.register(name='scenes', url='/scenes/')
@cross_origin()
class SceneView(ResourceView):
    resource = SceneResource
    methods = [methods.Fetch, methods.List]


@api.register(name='ui', url='/ui/')
@cross_origin()
class UITranslationsView(ResourceView):
    resource = UITranslationsResource
    methods = [methods.Fetch, methods.List]
