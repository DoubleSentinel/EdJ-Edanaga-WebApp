from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_mongorest import MongoRest, methods
from flask_mongorest.views import ResourceView

from resources import SceneResource, UITranslationsResource, TestUserResource, IsUserResource

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


@api.register(name='ui', url='/ui/')
class UITranslationsView(ResourceView):
    resource = UITranslationsResource
    methods = [methods.Fetch, methods.List]


@api.register(name='user', url='/testing_user/')
class TestUserView(ResourceView):
    resource = TestUserResource
    methods = [methods.Create, methods.Fetch]


@api.register(name='isuser', url='/is_user/')
class IsUserView(ResourceView):
    resource = IsUserResource
    methods = [methods.List]
