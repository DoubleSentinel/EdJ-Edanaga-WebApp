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


class UIText(Document):
    target_ui_name = StringField()
    language = StringField()
    text = StringField()
    description = StringField()

    def __unicode__(self):
        return f"{self.target_ui_name}_{self.language.upper()}"


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
