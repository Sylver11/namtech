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
