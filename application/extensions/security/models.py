from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from application.database import db, UUID
from datetime import datetime
import uuid as uuid_ext

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

#role_ability_assoc = db.Table('na_user_role_ability_assoc',
#        db.Column('id', db.Integer(), primary_key=True),
#        db.Column(
#            'role_uuid',
#            UUID,
#            db.ForeignKey('na_user_role.uuid'),
#            primary_key=True),
#        db.Column(
#            'ability_uuid',
#            UUID,
#            db.ForeignKey('na_user_role_ability.uuid'),
#            primary_key=True),
#        extend_existing=True)


#class Ability(db.Model):
#    __tablename__ = 'na_user_role_ability'
#    __table_args__ = {'extend_existing': True}
#    uuid = db.Column(
#            UUID(),
#            primary_key=True,
#            default=uuid_ext.uuid4)
#    name = db.Column(db.String(120), unique=True)
#    created = db.Column(db.DateTime, default=datetime.utcnow)
#    updated = db.Column(db.DateTime,
#            default=datetime.utcnow,
#            onupdate=datetime.utcnow)
#
    #def __init__(self, name):
    #    self.name = name.lower()


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
#    abilities = relationship(
#            'Ability',
#            secondary=role_ability_assoc,
#            backref=db.backref('roles', lazy='dynamic'))

#    def __init__(self, name):
#        self.name = name.lower()

#    def add_abilities(self, *abilities):
#        for ability in abilities:
#            existing_ability = Ability.query.filter_by(
#                name=ability).first()
#            if not existing_ability:
#                existing_ability = Ability(ability)
#                db.session.add(existing_ability)
#                db.session.commit()
#            self.abilities.append(existing_ability)
#
#    def remove_abilities(self, *abilities):
#        for ability in abilities:
#            existing_ability = Ability.query.filter_by(name=ability).first()
#            if existing_ability and existing_ability in self.abilities:
#                self.abilities.remove(existing_ability)


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

