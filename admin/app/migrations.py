import os, re
from flask import Flask

from flask_mongoengine import MongoEngine
from mongoengine import errors as mongoerrors

from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import encrypt_password

from auth.models import User, Role

from crud.models import (Languages,
                         ObjectiveName,
                         Objective,
                         ConstantVariables,
                         UITranslations,
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
    ## Languages
    english = Languages(name="EN").save()
    french = Languages(name="FR").save()
    german = Languages(name="DE").save()
    italian = Languages(name="IT").save()
    languages = {english.name: english, french.name: french, german.name: german, italian.name: italian}
    ## Objectives
    objective0 = ObjectiveName(unity_name="objective0", name="pnitro").save()
    objective1 = ObjectiveName(unity_name="objective1", name="micro").save()
    objective2 = ObjectiveName(unity_name="objective2", name="recovp").save()
    objective3 = ObjectiveName(unity_name="objective3", name="wat").save()
    objective4 = ObjectiveName(unity_name="objective4", name="energ").save()
    objective5 = ObjectiveName(unity_name="objective5", name="illn").save()
    objective6 = ObjectiveName(unity_name="objective6", name="attrac").save()
    objective7 = ObjectiveName(unity_name="objective7", name="timeuser").save()
    objective8 = ObjectiveName(unity_name="objective8", name="cost").save()
    objective9 = ObjectiveName(unity_name="objective9", name="flex").save()
    ## Variable Sets
    ConstantVariables(name="default",
                      variable_set=[
                          Objective(name=objective0,
                                    description="High removal of nitrogen compounds",
                                    unit="%",
                                    worst=20,
                                    best=90,
                                    value_fun_shape="exponential",
                                    global_weight=0.08662175168),
                          Objective(name=objective1,
                                    description="High removal of micropolluants",
                                    unit="%",
                                    worst=7,
                                    best=90,
                                    value_fun_shape="linear",
                                    global_weight=0.01732435034),
                          Objective(name=objective2,
                                    description="High nutrient recovery for fertilizer",
                                    unit="%",
                                    worst=0,
                                    best=81 + 1 / 3,
                                    value_fun_shape="linear",
                                    global_weight=0.06929740135),
                          Objective(name=objective3,
                                    description="Low use of water",
                                    unit="l/p*day",
                                    worst=26.6,
                                    best=0,
                                    value_fun_shape="linear",
                                    global_weight=0.07795957652),
                          Objective(name=objective4,
                                    description="Low net energy consumption",
                                    unit="kWh/p*year",
                                    worst=279.7269231,
                                    best=15,
                                    value_fun_shape="linear",
                                    global_weight=0.06929740135),
                          Objective(name=objective5,
                                    description="High health protection",
                                    unit="times/year",
                                    worst=5,
                                    best=0,
                                    value_fun_shape="linear",
                                    global_weight=0.06063522618),
                          Objective(name=objective6,
                                    description="High attractiveness",
                                    unit="points",
                                    worst=3,
                                    best=10,
                                    value_fun_shape="linear",
                                    global_weight=0.09624639076),
                          Objective(name=objective7,
                                    description="Low time demand for end-users",
                                    unit="h/year",
                                    worst=24.225,
                                    best=0,
                                    value_fun_shape="exponential",
                                    global_weight=0.06737247353),
                          Objective(name=objective8,
                                    description="Low annual costs",
                                    unit="CHF/p*year",
                                    worst=636,
                                    best=153,
                                    value_fun_shape="exponential",
                                    global_weight=0.09624639076),
                          Objective(name=objective9,
                                    description="High flexibility (intergenerational equity)",
                                    unit="years",
                                    worst=24.9,
                                    best=5,
                                    value_fun_shape="linear",
                                    global_weight=0.03368623677),
                      ]).save()
    ## HomeScreens
    HomeScreen(language=english,
               welcome_title="Welcome to Edanaga.ch",
               welcome_text="Home of the Eawag project meant to collect population consensus on water treatement "
                            "solutions in rural areas of Switzerland. If you want to participate in the testing "
                            "environment, you should have been given a specific link to access the test.").save()
    HomeScreen(language=french,
               welcome_title="Bienvenue sur Edanaga.ch",
               welcome_text="Accueil du projet Eawag destiné à collecter un consensus de la population sur les "
                            "solutions de traitement des eaux usagé en zones rurales de la Suisse. Si vous "
                            "souhaitez participer dans l'environnement de test, vous devriez avoir reçu un lien "
                            "spécifique pour accéder au test.").save()
    HomeScreen(language=german,
               welcome_title="Willkommen bei Edanaga.ch",
               welcome_text="Heimat des Eawag-Projekts zum Sammeln Bevölkerungskonsens über "
                            "Wasseraufbereitungslösungen in ländliche Gebiete der Schweiz. Wenn Sie teilnehmen "
                            "möchten In der Testumgebung sollten Sie eine erhalten haben spezifischer Link, "
                            "um auf den Test zuzugreifen.").save()
    HomeScreen(language=italian,
               welcome_title="Benvenuti su Edanaga.ch",
               welcome_text="Sede del progetto Eawag destinato a raccogliere consenso della popolazione sulle "
                            "soluzioni di trattamento delle acque nel 2005 zone rurali della Svizzera. Se vuoi "
                            "partecipare nell'ambiente di test, avresti dovuto ricevere un link specifico per "
                            "accedere al test.").save()
    ## Unity
    ## Conversations
    header_title = r"title\([0-9a-zA-Z_.]+\)"
    header_language = r"language\([A-Z]{2}\)"
    target_tag = r"tgt\(\w+\)"
    position_tag = r"pos\([0-9]+\)"
    in_parentheses = r'\((.*?)\)'
    for filename in os.listdir('./text_migrations'):
        with open('./text_migrations/' + filename) as file:
            lang = ""
            title = ""
            conversation_block = []
            for line in file:
                if line in ["\n", "\r\n"]:
                    if re.match(header_title, conversation_block[0]):
                        title = re.search(in_parentheses, conversation_block[0]).group(1)
                    if re.match(header_language, conversation_block[1]):
                        lang = re.search(in_parentheses, conversation_block[1]).group(1)

                    snippets = []
                    for block in conversation_block[2:]:
                        if re.match(target_tag, block):
                            tgt = re.search(in_parentheses, block).group(1)
                        elif re.match(position_tag, block):
                            pos = re.search(in_parentheses, block).group(1)
                        else:
                            snippets.append(Conversation(target_character=tgt,
                                                         position_in_conversation=pos,
                                                         text=block.rstrip()))
                    Scene(language=languages[lang],
                          conversation_title=title,
                          conversation_content=snippets).save()
                    conversation_block = []
                else:
                    conversation_block.append(line)

    ### UITranslations
    header_scene = r"scene\([0-9a-zA-Z_.]+\)"
    desc_tag = r"pos\([0-9]+\)"
    in_parentheses = r'\((.*?)\)'
    for filename in os.listdir('./ui_migrations'):
        with open('./ui_migrations/' + filename) as file:
            lang = ""
            scene = ""
            ui_block = []
            for line in file:
                if line in ["\n", "\r\n"]:
                    if re.match(header_scene, ui_block[0]):
                        scene = re.search(in_parentheses, ui_block[0]).group(1)
                    if re.match(header_language, ui_block[1]):
                        lang = re.search(in_parentheses, ui_block[1]).group(1)

                    ui_element = []
                    for block in ui_block[2:]:
                        if re.match(target_tag, block):
                            tgt = re.search(in_parentheses, block).group(1)
                        elif re.match(position_tag, block):
                            pos = re.search(in_parentheses, block).group(1)
                        else:
                            ui_element.append(UIElement(gameobject_id=tgt,
                                                        description=pos,
                                                        text_value=block.rstrip()))
                    UITranslations(language=languages[lang],
                                   scene=scene,
                                   elements=ui_element).save()
                    ui_block = []
                else:
                    ui_block.append(line)
    #### TitleScreen
    UITranslations(language=english,
                   scene="TitleScreen",
                   elements=[
                       UIElement(gameobject_id="inptPlaceholderUser",
                                 description="Username placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderPass",
                                 description="Password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="btnCreate",
                                 description="Create new account button",
                                 text_value="Sign up"),
                       UIElement(gameobject_id="btnLogin",
                                 description="Login button",
                                 text_value="Login"),
                       UIElement(gameobject_id="inptPlaceholderNewUser",
                                 description="Account creation username placeholder",
                                 text_value="New Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPass",
                                 description="Account creation password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPass",
                                 description="Account creation password confirmation placeholder",
                                 text_value="Confirm Password"),
                       UIElement(gameobject_id="btnConfirmCreate",
                                 description="Account creation submit button",
                                 text_value="Create Account"),
                       UIElement(gameobject_id="btnCancel",
                                 description="Account creation cancel button",
                                 text_value="Cancel"),
                       UIElement(gameobject_id="inptPlaceholderUsernameChange",
                                 description="Password change username input placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPassChange",
                                 description="Password change new password input placeholder",
                                 text_value="New Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPassChange",
                                 description="Password change confirm new password input placeholder",
                                 text_value="Confirm new password"),
                       UIElement(gameobject_id="btnConfirmChange",
                                 description="Account creation cancel button",
                                 text_value="Submit new password"),
                       UIElement(gameobject_id="btnCancelChange",
                                 description="Password change cancel button",
                                 text_value="Cancel"),
                   ]).save()
    UITranslations(language=french,
                   scene="TitleScreen",
                   elements=[
                       UIElement(gameobject_id="inptPlaceholderUser",
                                 description="Username placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderPass",
                                 description="Password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="btnCreate",
                                 description="Create new account button",
                                 text_value="Sign up"),
                       UIElement(gameobject_id="btnLogin",
                                 description="Login button",
                                 text_value="Login"),
                       UIElement(gameobject_id="inptPlaceholderNewUser",
                                 description="Account creation username placeholder",
                                 text_value="New Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPass",
                                 description="Account creation password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPass",
                                 description="Account creation password confirmation placeholder",
                                 text_value="Confirm Password"),
                       UIElement(gameobject_id="btnConfirmCreate",
                                 description="Account creation submit button",
                                 text_value="Create Account"),
                       UIElement(gameobject_id="btnCancel",
                                 description="Account creation cancel button",
                                 text_value="Cancel"),
                       UIElement(gameobject_id="inptPlaceholderUsernameChange",
                                 description="Password change username input placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPassChange",
                                 description="Password change new password input placeholder",
                                 text_value="New Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPassChange",
                                 description="Password change confirm new password input placeholder",
                                 text_value="Confirm new password"),
                       UIElement(gameobject_id="btnConfirmChange",
                                 description="Account creation cancel button",
                                 text_value="Submit new password"),
                       UIElement(gameobject_id="btnCancelChange",
                                 description="Password change cancel button",
                                 text_value="Cancel"),
                   ]).save()
    UITranslations(language=german,
                   scene="TitleScreen",
                   elements=[
                       UIElement(gameobject_id="inptPlaceholderUser",
                                 description="Username placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderPass",
                                 description="Password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="btnCreate",
                                 description="Create new account button",
                                 text_value="Sign up"),
                       UIElement(gameobject_id="btnLogin",
                                 description="Login button",
                                 text_value="Login"),
                       UIElement(gameobject_id="inptPlaceholderNewUser",
                                 description="Account creation username placeholder",
                                 text_value="New Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPass",
                                 description="Account creation password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPass",
                                 description="Account creation password confirmation placeholder",
                                 text_value="Confirm Password"),
                       UIElement(gameobject_id="btnConfirmCreate",
                                 description="Account creation submit button",
                                 text_value="Create Account"),
                       UIElement(gameobject_id="btnCancel",
                                 description="Account creation cancel button",
                                 text_value="Cancel"),
                       UIElement(gameobject_id="inptPlaceholderUsernameChange",
                                 description="Password change username input placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPassChange",
                                 description="Password change new password input placeholder",
                                 text_value="New Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPassChange",
                                 description="Password change confirm new password input placeholder",
                                 text_value="Confirm new password"),
                       UIElement(gameobject_id="btnConfirmChange",
                                 description="Account creation cancel button",
                                 text_value="Submit new password"),
                       UIElement(gameobject_id="btnCancelChange",
                                 description="Password change cancel button",
                                 text_value="Cancel"),
                   ]).save()
    UITranslations(language=italian,
                   scene="TitleScreen",
                   elements=[
                       UIElement(gameobject_id="inptPlaceholderUser",
                                 description="Username placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderPass",
                                 description="Password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="btnCreate",
                                 description="Create new account button",
                                 text_value="Sign up"),
                       UIElement(gameobject_id="btnLogin",
                                 description="Login button",
                                 text_value="Login"),
                       UIElement(gameobject_id="inptPlaceholderNewUser",
                                 description="Account creation username placeholder",
                                 text_value="New Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPass",
                                 description="Account creation password placeholder",
                                 text_value="Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPass",
                                 description="Account creation password confirmation placeholder",
                                 text_value="Confirm Password"),
                       UIElement(gameobject_id="btnConfirmCreate",
                                 description="Account creation submit button",
                                 text_value="Create Account"),
                       UIElement(gameobject_id="btnCancel",
                                 description="Account creation cancel button",
                                 text_value="Cancel"),
                       UIElement(gameobject_id="inptPlaceholderUsernameChange",
                                 description="Password change username input placeholder",
                                 text_value="Username"),
                       UIElement(gameobject_id="inptPlaceholderNewPassChange",
                                 description="Password change new password input placeholder",
                                 text_value="New Password"),
                       UIElement(gameobject_id="inptPlaceholderConfirmPassChange",
                                 description="Password change confirm new password input placeholder",
                                 text_value="Confirm new password"),
                       UIElement(gameobject_id="btnConfirmChange",
                                 description="Account creation cancel button",
                                 text_value="Submit new password"),
                       UIElement(gameobject_id="btnCancelChange",
                                 description="Password change cancel button",
                                 text_value="Cancel"),
                   ]).save()
exit(0)
