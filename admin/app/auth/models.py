from flask_security import UserMixin, RoleMixin
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    ListField,
    ReferenceField,
    StringField,
)
from mongoengine import Document


class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

    def __unicode__(self):
        return self.name


class User(Document, UserMixin):
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])

    def __unicode__(self):
        return self.email
