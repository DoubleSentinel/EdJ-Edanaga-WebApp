from models import UIText, Conversation, Scene

from flask_mongorest.resources import Resource


class ConversationResource(Resource):
    document = Conversation


class SceneResource(Resource):
    document = Scene
    related_resources = {
        'conversation': ConversationResource
    }

class UITextResource(Resource):
    document = UIText