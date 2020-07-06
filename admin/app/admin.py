import os
from flask import Flask, render_template, redirect, url_for, abort, request

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_wtf.csrf import CSRFProtect

from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import encrypt_password


from flask_admin import Admin, helpers
from flask_admin.menu import MenuLink

from auth.models import User, Role
from auth.views import SecuredHomeView, SuperUserView, SuperRoleView

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

# Add views to Flask Admin for CRUD handling of website data
#admin.add_view(MemberView(Member, MODEL_DESCRIPTIONS[Member][0]))

# Add views to Flask Admin for superuser to handle authentication
admin.add_view(SuperUserView(User, "Users", category="Administration"))
admin.add_view(SuperRoleView(Role, "User roles", category="Administration"))

# Adding links to handle session for users
admin.add_link(
    MenuLink(
        name="Logout",
        category="Session",
        url=app.config["SECURITY_LOGOUT_URL"]
    )
)
admin.add_link(
    MenuLink(
        name="",
        category="Session",
        url=app.config["SECURITY_CHANGE_URL"],
    )
)

# defining test users for development mode
if os.environ.get("FLASK_ENV", "") == "development":
    with app.app_context():
        try:
            user_role = Role(name="user").save()
            super_user_role = Role(name="superuser").save()
        except mongoerrors.NotUniqueError:
            user_role = Role.objects.get(name="user")
            super_user_role = Role.objects.get(name="superuser")
        try:
            User.objects.get(email="admin")
            print(
                "Test user already exists, no need to create.\n email= admin password= admin"
            )
        except mongoerrors.DoesNotExist:
            test_user = user_datastore.create_user(
                email="admin",
                password=encrypt_password("admin"),
                roles=[user_role, super_user_role],
            )
            print("Test user created as: email= admin password= admin")

