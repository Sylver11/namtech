""" This the heart of the application. From here
the application gets configured and build. """

def configure_logging(app):
    import logging
    #import logging.config
    root = logging.getLogger()
    if app.config['LOG_SENTRY_ACTIVE']:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        sentry_sdk.init(
            dsn=app.config['LOG_SENTRY_DSN'],
            integrations=[FlaskIntegration(),SqlalchemyIntegration()],
            traces_sample_rate=1.0
        )
    if app.config['LOG_MAIL_ACTIVE']:
        from application.logger import ThreadedSMTPHandler
        mailhost = app.config['LOG_MAIL_HOST']
        port = app.config['LOG_MAIL_PORT']
        fromaddr = app.config['LOG_MAIL_FROM_ADDRESS']
        toaddrs = app.config['LOG_MAIL_TO_ADDRESS']
        username = app.config['LOG_MAIL_USERNAME']
        password = app.config['LOG_MAIL_PASSWORD']
        mail_handler = ThreadedSMTPHandler(
            mailhost=(mailhost,port),
            fromaddr=fromaddr,
            toaddrs=toaddrs,
            credentials=(username,password),
            subject='Application Error')
        mail_handler.setLevel(logging.ERROR)
        logging.getLogger('werkzeug').addHandler(mail_handler)
        root.addHandler(mail_handler)
        app.logger.addHandler(mail_handler)
    if app.config['LOG_DATABASE_ACTIVE']:
        from application.logger import SQLAlchemyHandler
        database_handler = SQLAlchemyHandler()
        database_handler.setLevel(logging.ERROR)
        logging.getLogger('werkzeug').addHandler(database_handler)
        app.logger.addHandler(database_handler)
        root.addHandler(database_handler)

    @app.errorhandler(500)
    def internal_server_error(error):
        original_error = getattr(error, "original_exception", None)
        if original_error is None:
            do = "dummy"
            print('original exception is none')
        print(original_error)
        return error, 500

def init_extensions(app):
    #from flask_admin import Admin
    #admin = Admin(app, name='', template_mode='bootstrap5')
    from flask_security import SecurityManager, UserDatastore
    from application.database import db
    user_datastore = UserDatastore(db)
    security_manager = SecurityManager(app, user_datastore)


def init_vendors(app):
    #from flask_mail import Mail
    from flask_assets import Environment
    from application.assets import compile_assets
    from application.database import db
    assets = Environment()
    assets.init_app(app)
    compile_assets(assets)
    db.init_app(app)
    db.create_all()
    #Mail(app)


def register_blueprints(app):
    from werkzeug.utils import find_modules, import_string
    for name in find_modules(__name__, include_packages=True, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

#def add_error_page(app):
#    @app.errorhandler(500)
#    def internal_server_error(error):
#        return error, 500

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
