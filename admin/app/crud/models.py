import datetime
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    IntField,
    FloatField,
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
    conversation_title = StringField()
    conversation_content = ListField(EmbeddedDocumentField(Conversation))

    def __unicode__(self):
        return f"{self.conversation_title}_{self.language.name.upper()}"


class TestUser(Document):
    language_preference = StringField()
    username = StringField(required=True, unique=True)
    userpass = StringField(required=True)
    last_login = DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return f"{self.username}"


class ObjectiveName(Document):
    unity_name = StringField(required=True)
    name = StringField(required=True)

    def __unicode__(self):
        return self.name


class Objective(EmbeddedDocument):
    name = ReferenceField(ObjectiveName)
    description = StringField()
    unit = StringField(required=True)
    worst = FloatField(required=True)
    best = FloatField(required=True)
    value_fun_shape = StringField(required=True)
    global_weight = FloatField(required=True)


class ConstantVariables(Document):
    name = StringField()
    variable_set = ListField(EmbeddedDocumentField(Objective))

    def __unicode__(self):
        return f"{self.name}"


class Invitations(Document):
    token_url = StringField(unique=True, required=True)
    active = BooleanField()
    creation_date = DateTimeField(default=datetime.datetime.utcnow)
    # TODO: remove delete_rule and change Invitiation View handling when deleting a view
    # to delete all participants as well
    participants = ListField(ReferenceField(TestUser, reverse_delete_rule=CASCADE))
    constant_variables = ReferenceField(ConstantVariables, default="default")
