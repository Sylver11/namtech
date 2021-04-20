from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql.base import MSBinary
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import types
from dataclasses import dataclass
from datetime import datetime
import uuid


db = SQLAlchemy()

class UUID(types.TypeDecorator):
    impl = MSBinary
    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self,length=self.impl.length)

    def process_bind_param(self,value,dialect=None):
        try:
            return value.bytes
        except AttributeError:
            try:
                return uuid.UUID(value).bytes
            except TypeError:
                return value

    def process_result_value(self,value,dialect=None):
        if value is None:
            return value
        try:
            return uuid.UUID(bytes=value)
        except TypeError:
            return uuid.UUID(value)


#j@dataclass
class Base(db.Model):
#    uuid:str
#    created:datetime
#    updated:datetime
    __table_args__ = {'extend_existing': True}
    __abstract__ = True
    uuid = db.Column(
            UUID(),
            primary_key=True,
            default=uuid.uuid4)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)


class Datastore:
    def __init__(self):
        self.db = db

    def commit(self):
        self.db.session.commit()

    def get(self, model, identifier=None):
        if identifier:
            return model.query.filter_by(identifier)
        return model.query.all()

    def put(self, model):
        self.db.session.add(model)
        return model

    def merge(self, model):
        self.db.session.merge(model)
        return model

    def delete(self, model):
        self.db.session.delete(model)

