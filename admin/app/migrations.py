import os
from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import encrypt_password

from auth.models import User, Role

from crud.models import (UITranslations,
                         UIElement,
                         Conversation,
                         Scene,
                         HomeScreen,
                         Invitations)

app = Flask(__name__)

# configuration from file
app.config.from_pyfile("./config.py")

# Flask MongoEngine connection
db = MongoEngine(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    # creating first admin super user
    try:
        user_role = Role(name="user").save()
        super_user_role = Role(name="superuser").save()
    except mongoerrors.NotUniqueError:
        user_role = Role.objects.get(name="user")
        super_user_role = Role.objects.get(name="superuser")
    try:
        User.objects.get(email=app.config["ADMINUSER"])
    except mongoerrors.DoesNotExist:
        test_user = user_datastore.create_user(
            email=app.config["ADMINUSER"],
            password=encrypt_password(app.config["ADMINPASS"]),
            roles=[user_role, super_user_role],
        )
    except mongoerrors.MultipleObjectsReturned:
        User.objects(email=app.config["ADMINUSER"]).first().delete()

    # Migrations
    ## HomeScreens
    try:
        HomeScreen(language="EN",
                   welcome_title="Welcome to Edanaga.ch",
                   welcome_text="""Home of the Eawag project meant to collect 
                   population consensus on water treatement solutions in
                   rural areas of Switzerland. If you want to participate
                   in the testing environment, you should have been given a
                   specific link to access the test.""").save()

        HomeScreen(language="FR",
                   welcome_title="Bienvenue sur Edanaga.ch",
                   welcome_text="""Accueil du projet Eawag destiné à collecter
                    un consensus de la population sur les solutions de traitement
                    des eaux usagé en zones rurales de la Suisse. Si vous souhaitez
                    participer dans l'environnement de test, vous devriez avoir reçu
                    un lien spécifique pour accéder au test.""").save()
        HomeScreen(language="DE",
                   welcome_title="Willkommen bei Edanaga.ch",
                   welcome_text="""Heimat des Eawag-Projekts zum Sammeln
                    Bevölkerungskonsens über Wasseraufbereitungslösungen in
                    ländliche Gebiete der Schweiz. Wenn Sie teilnehmen möchten
                    In der Testumgebung sollten Sie eine erhalten haben
                    spezifischer Link, um auf den Test zuzugreifen.""").save()
        HomeScreen(language="IT",
                   welcome_title="Benvenuti su Edanaga.ch",
                   welcome_text="""Sede del progetto Eawag destinato a raccogliere
                    consenso della popolazione sulle soluzioni di trattamento delle acque nel 2005
                    zone rurali della Svizzera. Se vuoi partecipare
                    nell'ambiente di test, avresti dovuto ricevere un
                    link specifico per accedere al test..""").save()
        exit(0)
    except Exception as e:
        print(str(e))
        exit(1)
