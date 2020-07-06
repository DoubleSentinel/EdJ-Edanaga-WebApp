from flask import url_for, redirect, abort, request

from mongoengine import errors as mongoerrors

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.base import AdminIndexView, expose

from flask_security.utils import encrypt_password
from flask_security import current_user

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, HiddenField

from auth.models import User, Role

from utility import UserAccessFactory


class SecuredHomeView(UserAccessFactory('user'), AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        return self.render('index.html')

class SuperUserView(UserAccessFactory('superuser'), ModelView):

    column_list = [
                "email",
                "roles",
            ]

    def on_model_change(self, form, model, is_created):
        # overriding this function to ensure the password is encrypted in
        # db when a user is edited from flask-admin
        if is_created:
            model.password = encrypt_password(model.password)


class SuperRoleView(UserAccessFactory('superuser'), ModelView):
    pass
