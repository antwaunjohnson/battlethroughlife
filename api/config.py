import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "supersekrit"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql+psycopg2://aj:asdfasdf@localhost/battledb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
