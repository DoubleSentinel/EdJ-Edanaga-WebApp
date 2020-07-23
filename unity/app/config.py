import os

MONGODB_SETTINGS = {
    'db': os.environ.get("MONGODB"),
    'username': os.environ.get("MONGOUSER"),
    'password': os.environ.get("MONGOPASS"),
    'host': os.environ.get("MONGOHOST")
}
