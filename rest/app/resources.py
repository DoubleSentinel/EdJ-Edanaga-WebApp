from models import Languages, UITranslations, UIElement, Conversation, Scene

from flask_mongorest.resources import Resource
from flask_mongorest import operators


class LanguagesResource(Resource):
    document = Languages


class ConversationResource(Resource):
    document = Conversation


class UIElementResource(Resource):
    document = UIElement


class SceneResource(Resource):
    document = Scene
    related_resources = {
        'conversation': ConversationResource,
        'language': LanguagesResource,
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
        'elements': UIElementResource,
        'language': LanguagesResource,
    }

    filters = {
        'language': [operators.Exact],
        'scene': [operators.Exact]
    }
