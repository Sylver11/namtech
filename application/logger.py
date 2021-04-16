#import os
import logging
import traceback
from application.models import Log
from application.database import db
from threading import Thread
#from email.message import EmailMessage
#import email.utils
#import smtplib

class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        db.session.add(log)
        db.session.commit()

class ThreadedSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        thread = Thread(target=super().emit,args=(record,))
        thread.start()
