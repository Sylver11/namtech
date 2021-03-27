from flask_login import LoginManager
from flask import Blueprint
from application.database import db
from .models import User, Group, Role
from .security_manager__settings import SecurityManager__Settings
from .security_manager__views import SecurityManager__Views
from .security_manager__utils import SecurityManager__Utils

class SecurityManager(SecurityManager__Settings,
        SecurityManager__Views,
        SecurityManager__Utils):

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_security(app)

    def init_security(self, app):
        app.manager = self

        self.login_manager = LoginManager(app)
        self.login_manager.login_view = 'security_bp.login'
        @self.login_manager.user_loader
        def load_user(uuid):
            return User.query.filter_by(uuid=uuid).first()

        blueprint = Blueprint(
                'security_bp',
                __name__,
                template_folder='templates',
                static_folder='static',)

        app.register_blueprint(blueprint)

        self._add_url_routes(app)

        from .cli import security_cli
        app.cli.add_command(security_cli)

        if self.USER_SET_DB_DEFAULTS:
            role_name = self.USER_DEFAULT_ROLE_NAME
            role_description = self.USER_DEFAULT_ROLE_DESCRIPTION

            @app.before_request
            def check_security_db_defaults():
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    role = Role(name=role_name, description=role_description)
                    db.session.add(role)
                db.session.commit()


    def deactivate_user(self, user):
        pass

    def activate_user(self, user):
        pass

    def create_role(self, **kwargs):
        pass

    def find_or_create_role(self, name, **kwargs):
        pass

    def get_user_by_email(self, email):
        if email:
            user = User.query.filter_by(email=email).first()
            return user
        users = User.query.all()
        return users

    def get_group_by_name(self, name):
        group = Group.query.filter_by(name=name).first()
        return group

    def user_part_of_default_group(self, user_model):
        name = self.USER_DEFAULT_GROUP_NAME
        default_group = self.get_group_by_name(name)
        if not default_group:
            return False
        if default_group.uuid == user_model.group_uuid:
            return True
        return False


    def add_user(self, user_model):
        from sqlalchemy.exc import IntegrityError
        try:
            new_user = db.session.add(user_model)
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            return 'User already exists'
        return user_model

    def update_user(self, user):
        user = db.session.merge(user)
        db.session.commit()
        return user

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()
        return None

    def add_group(self, group_model):
        from sqlalchemy.exc import IntegrityError
        try:
            new_group = db.session.add(group_model)
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            return 'Group already exists'
        return group_model


    def _add_url_routes(self, app):

        def test_stub():
            return self.test_view()

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_view()


        app.add_url_rule(self.USER_TEST_URL, 'user_bp.test', test_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_REGISTER_URL, 'user_bp.register', register_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGOUT_URL, 'user_bp.logout', logout_stub, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGIN_URL, 'user_bp.login', login_stub, methods=['GET', 'POST'])

