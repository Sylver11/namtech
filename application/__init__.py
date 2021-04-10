""" This the heart of the application. From here
the application gets configured and build. """

def init_extensions(app):
    from flask_security import SecurityManager, UserDatastore
    from application.database import db
    user_datastore = UserDatastore(db)
    #from application.extensions.flask-security import SecurityManager
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
    with app.app_context():
        register_blueprints(app)
        init_extensions(app)
        init_vendors(app)
        run_migration(app)
        return app
