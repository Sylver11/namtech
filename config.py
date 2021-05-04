from os import environ, path
from dotenv import load_dotenv
from logging.config import dictConfig

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEVELOPMENT = True
    DEBUG = True
    FLASK_DEBUG = 1
    SECRET_KEY = environ.get('SECRET_KEY')
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    DB_DEFAULT_VALUES_ACTIVE = environ.get('DB_DEFAULT_VALUES_ACTIVE','false').lower() == 'true'
    LOG_DATABASE_ACTIVE = environ.get('LOG_DATABASE_ACTIVE','false').lower() == 'true'
    LOG_SENTRY_ACTIVE = environ.get('LOG_SENTRY_ACTIVE','false').lower() == 'true'
    LOG_SENTRY_DSN = environ.get('LOG_SENTRY_DSN')
    LOG_MAIL_ACTIVE = environ.get('LOG_MAIL_ACTIVE','false').lower() == 'true'
    LOG_MAIL_HOST = environ.get('LOG_MAIL_HOST')
    LOG_MAIL_PORT = environ.get('LOG_MAIL_PORT')
    LOG_MAIL_USERNAME = environ.get('LOG_MAIL_USERNAME')
    LOG_MAIL_PASSWORD = environ.get('LOG_MAIL_PASSWORD')
    LOG_MAIL_FROM_ADDRESS = environ.get('LOG_MAIL_FROM_ADDRESS')
    LOG_MAIL_TO_ADDRESS = environ.get('LOG_MAIL_TO_ADDRESS')


class ConfigProduction(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False
    SERVER_NAME = environ.get('SERVER_NAME')
    SERVER_ADMIN_MAIL = environ.get('SERVER_ADMIN_MAIL')


class ConfigTesting(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_SQLALCHEMY_DATABASE_URI')

