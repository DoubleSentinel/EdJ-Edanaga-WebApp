import os

MONGODB_SETTINGS = {
    'db': os.environ.get("MONGODB"),
    'username': os.environ.get("MONGOUSER"),
    'password': os.environ.get("MONGOPASS"),
    'host': os.environ.get("MONGOHOST")
}

ADMINUSER = os.environ.get("ADMINUSER")
ADMINPASS = os.environ.get("ADMINPASS")

SECRET_KEY = os.environ.get("SECRET_KEY")

SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

SECURITY_CHANGEABLE = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_CHANGE_URL = '/change'
SECURITY_LOGIN_URL = '/login'
SECURITY_LOGOUT_URL = '/logout'
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_POST_LOGOUT_VIEW = '/login'

