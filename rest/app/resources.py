from models import Languages, UITranslations, UIElement, Conversation, Scene, TestUser

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
        'conversation_content': ConversationResource,
        'language': LanguagesResource,
    }

    filters = {
        'conversation_title': [operators.Exact]
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


class TestUserResource(Resource):
    document = TestUser
    related_resources = {
        'language': LanguagesResource,
    }


class IsUserResource(Resource):
    document = TestUser
    fields = ['id', 'username']

    filters = {
        'username': [operators.Exact]
    }
