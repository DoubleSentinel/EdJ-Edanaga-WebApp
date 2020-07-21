from models import UITranslations, UIElement, Conversation, Scene

from flask_mongorest.resources import Resource
from flask_mongorest import operators


class ConversationResource(Resource):
    document = Conversation


class UIElementResource(Resource):
    document = UIElement


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


class UITranslationsResource(Resource):
    document = UITranslations

    related_resources = {
        'elements': UIElementResource
    }

    filters = {
        'language': [operators.Exact],
        'scene': [operators.Exact]
    }
