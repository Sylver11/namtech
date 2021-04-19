from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from application.database import db, UUID
from datetime import datetime
import uuid as uuid_ext

class Log(db.Model):
    __tablename__ = 'na_logs'
    uuid = db.Column(
            UUID(),
            primary_key=True,
            default=uuid_ext.uuid4)
    logger = db.Column(db.String(255))
    level = db.Column(db.String(255))
    trace = db.Column(db.Text)
    msg = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])


user_role_assoc = db.Table('na_user_role_assoc',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column(
            'user_uuid',
            UUID,
            db.ForeignKey('na_user.uuid'),
            primary_key=True),
        db.Column(
            'role_uuid',
            UUID,
            db.ForeignKey('na_user_role.uuid'),
            primary_key=True),
        extend_existing=True)

role_hierachy_assoc = db.Table('na_user_role_hierachy_assoc',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column(
            'parent_role_uuid',
            UUID,
            db.ForeignKey('na_user_role.uuid'),
            primary_key=True),
        db.Column(
            'child_role_uuid',
            UUID,
            db.ForeignKey('na_user_role.uuid'),
            primary_key=True),
        extend_existing=True)

class Role(db.Model):
    __tablename__ = 'na_user_role'
    __table_args__ = {'extend_existing': True}
    uuid = db.Column(
            UUID(),
            primary_key=True,
            default=uuid_ext.uuid4)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    child_roles = relationship(
            'Role',
            secondary= role_hierachy_assoc,
            primaryjoin=uuid==role_hierachy_assoc.c.parent_role_uuid,
            secondaryjoin=uuid==role_hierachy_assoc.c.child_role_uuid,
            backref="parent_roles")

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'na_user'
    __table_args__ = {'extend_existing': True}
    uuid = db.Column(
            UUID(),
            primary_key=True,
            default=uuid_ext.uuid4)
    firstname = db.Column(db.String(255),index=True, nullable=False)
    secondname = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    thirdparty_authenticated = db.Column(db.Boolean, nullable=False,
            default=False)
    thirdparty_name = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    roles = relationship('Role', secondary=user_role_assoc,
            backref=db.backref('users', lazy='dynamic'))
    group_uuid = db.Column(UUID, db.ForeignKey('na_user_group.uuid'))
    group = relationship('Group', back_populates='users')
    group_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

    def get_id(self):
        return self.uuid

    def is_authenticated(self):
        return self.authenticated

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.active

    def add_roles(self, *roles):
        self.roles.extend([role for role in roles if role not in self.roles])

    def remove_roles(self, *roles):
        self.roles = [role for role in self.roles if role not in roles]

    def has_roles(self, *requirements):
        role_names = self.roles
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in role_names:
                        authorized = True
                        break
                if not authorized:
                    return False
            else:
                role_name = requirement
                if not role_name in role_names:
                    return False
        return True


class Group(db.Model):
    __tablename__ = 'na_user_group'
    __table_args__ = {'extend_existing': True}
    uuid = db.Column(
            UUID(),
            primary_key=True,
            default=uuid_ext.uuid4)

    name = db.Column(db.String(255),index=True, unique= True, nullable=False)
    users = relationship('User', back_populates='group')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

