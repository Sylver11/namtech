""" This the heart of the application. From here
the application gets configured and build. """

def configure_logging(app):
    import logging
    import logging.config
    #from logging.handlers import SMTPHandler
    from application.logger import mail_handler
    logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)
    loggers = [app.logger, logging.getLogger('sqlalchemy'),
            logging.getLogger('werkzeug')]
    for logger in loggers:
        logger.add(
        if app.config['DATABASE_ERROR_LOG']:
            logger.add(sql_alchemy_handler)
        if app.config['MAIL_ERRORS']:
            logger.addHandler(mail_handler)

def init_extensions(app):
    from flask_admin import Admin
    admin = Admin(app, name='', template_mode='bootstrap5')
    from flask_security import SecurityManager, UserDatastore
    from application.database import db
    user_datastore = UserDatastore(db)
    security_manager = SecurityManager(app, user_datastore)


def init_vendors(app):
    from flask_mail import Mail
    from flask_assets import Environment
    from application.assets import compile_assets
    from application.database import db
    assets = Environment()
    assets.init_app(app)
    compile_assets(assets)
    db.init_app(app)
    db.create_all()
    Mail(app)


def register_blueprints(app):
    from werkzeug.utils import find_modules, import_string
    for name in find_modules(__name__, include_packages=True, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

def add_error_page(app):
    @app.errorhandler(500)
    def internal_server_error(error):
        return error, 500

def run_migration(app):
    from application.database import db
    from flask_migrate import Migrate
    return Migrate(app, db)


def create_app(env=''):
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('config.Config' + env)
    configure_logging(app)
    with app.app_context():
        register_blueprints(app)
        init_extensions(app)
        init_vendors(app)
        run_migration(app)
        return app
