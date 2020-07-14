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


class UIElement(EmbeddedDocument):
    gameobject_id = StringField()
    description = StringField()
    text_value = StringField()


class UITranslations(Document):
    language = StringField()
    scene = StringField()
    elements = ListField(EmbeddedDocumentField(UIElement))

    def __unicode__(self):
        return f"{self.scene}_{self.language.upper()}"


class Conversation(EmbeddedDocument):
    target_character = StringField()
    position_in_conversation = IntField()
    text = StringField()

    def __unicode__(self):
        return f"{self.target_character}"


class Scene(Document):
    unity_scene_name = StringField()
    language = StringField()
    conversation = ListField(EmbeddedDocumentField(Conversation))

    def __unicode__(self):
        return f"{self.unity_scene_name}_{self.language.upper()}"
