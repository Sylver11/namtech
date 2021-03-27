from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEVELOPMENT = True
    DEBUG = True
    FLASK_DEBUG = 1
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    SERVER_NAME = environ.get('SERVER_NAME')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_ERRORS = True
    ADMIN = environ.get('SERVER_ADMIN')


class ConfigProduction(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class ConfigTesting(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_TEST_DATABASE_URI")
