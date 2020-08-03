import os
from flask import Flask, render_template, redirect, url_for, abort, request, send_from_directory

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_wtf.csrf import CSRFProtect

from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import encrypt_password

from flask_admin import Admin, helpers
from flask_admin.menu import MenuLink

from auth.models import User, Role
from auth.views import SecuredHomeView, SuperUserView, SuperRoleView

from crud.models import (UITranslations,
                         UIElement,
                         Conversation,
                         Scene,
                         HomeScreen,
                         Invitations)
from crud.views import (UITranslationsView,
                        ConversationView,
                        SceneView,
                        HomeScreenView,
                        InvitationsView,
                        )

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# CSRF init
csrf = CSRFProtect(app)

# Create Flask-Admin support
admin = Admin(
    app,
    "Edanaga",
    index_view=SecuredHomeView(url="/"),
    template_mode='bootstrap3'
)


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for,
    )


# Add views to Flask Admin for CRUD handling of website data
admin.add_view(UITranslationsView(UITranslations, "UI Translations", category="Game Content"))
admin.add_view(SceneView(Scene, "Scenes' Translations", category="Game Content"))
admin.add_view(HomeScreenView(HomeScreen, "Home Screen Content", category="Public Website Content"))
admin.add_view(InvitationsView(Invitations, "Invitation links", category="Public Website Content"))

# Add views to Flask Admin for superuser to handle authentication
admin.add_view(SuperUserView(User, "Users", category="Administration"))
admin.add_view(SuperRoleView(Role, "User roles", category="Administration"))

admin.add_link(
    MenuLink(
        name="Change password",
        category="Session",
        url=app.config["SECURITY_CHANGE_URL"],
    )
)
# Adding links to handle session for users
admin.add_link(
    MenuLink(
        name="Logout",
        category="Session",
        url=app.config["SECURITY_LOGOUT_URL"]
    )
)


