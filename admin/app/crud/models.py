from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from mongoengine import Document, EmbeddedDocument, CASCADE, PULL


class Languages(Document):
    name = StringField(unique=True)

    def __unicode__(self):
        return self.name


class HomeScreen(Document):
    language = ReferenceField(Languages, unique=True)
    welcome_title = StringField()
    welcome_text = StringField()


class Invitations(Document):
    token_url = StringField()
    active = BooleanField()


class UIElement(EmbeddedDocument):
    gameobject_id = StringField()
    description = StringField()
    text_value = StringField()


class UITranslations(Document):
    language = ReferenceField(Languages)
    scene = StringField()
    elements = ListField(EmbeddedDocumentField(UIElement))

    def __unicode__(self):
        return f"{self.scene}_{self.language.name.upper()}"


class Conversation(EmbeddedDocument):
    target_character = StringField()
    position_in_conversation = IntField()
    text = StringField()

    def __unicode__(self):
        return f"{self.target_character}"


class Scene(Document):
    language = ReferenceField(Languages)
    unity_scene_name = StringField()
    conversation = ListField(EmbeddedDocumentField(Conversation))

    def __unicode__(self):
        return f"{self.unity_scene_name}_{self.language.name.upper()}"


class TestUser(Document):
    language_preference = ReferenceField(Languages)
    username = StringField(required=True, unique=True)
    userpass = StringField(required=True)
