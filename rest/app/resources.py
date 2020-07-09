from models import UIText, Conversation, Scene

from flask_mongorest.resources import Resource
from flask_mongorest import operators


class ConversationResource(Resource):
    document = Conversation


class SceneResource(Resource):
    document = Scene
    related_resources = {
        'conversation': ConversationResource
    }

    filters = {
        'scene': [operators.Exact]
    }

    rename_fields = {
        'unity_scene_name': 'scene'
    }


class UITextResource(Resource):
    document = UIText
