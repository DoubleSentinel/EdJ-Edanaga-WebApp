from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    GenericReferenceField,
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


class Conversation(Document):
    target_character = StringField()
    position_in_conversation = IntField()
    text = StringField()

    def __unicode__(self):
        return f"{self.target_character}"


class Scene(Document):
    unity_scene_name = StringField()
    language = StringField()
    conversation = ListField(ReferenceField(Conversation, reverse_delete_rule=PULL))

    def __unicode__(self):
        return f"{self.unity_scene_name}_{self.language.upper()}"
#
# class MemberOverride(EmbeddedDocument):
#    member = ReferenceField(Member,
#                            required=True, )
#    role = StringField(default="")
#
#    backstage = BooleanField(default=False)
#
#    # these properties are meant to simplify access to the referenced member's
#    # data to simplify templating macros (ex: templates/macros/members:list_members())
#
#    @property
#    def id(self):
#        return self.member.id
#
#    @property
#    def last_name(self):
#        return self.member.last_name
#
#    @property
#    def first_name(self):
#        return self.member.first_name
#
#    @property
#    def avatar(self):
#        return self.member.avatar
#
#    @property
#    def priority(self):
#        return self.member.priority
#
#    def thumbnail(self):
#        return self.member.thumbnail()
#
#    def __unicode__(self):
#
#        result = self.first_name + " " + self.last_name
#        if self.role:
#            result += ' - ' + self.role
#        if self.backstage:
#            result += ' - (backstage)'
#
#        return result
