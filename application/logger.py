from Flask import current_app
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import traceback
from models import Log
from database import db
from email.message import EmailMessage
import email.utils

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


class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg, self.fromaddr, self.toaddrs)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)



mail_handler = SMTPHandler(
        mailhost=(current_app.config['MAIL_HOST'],app.config['MAIL_PORT']),
        fromaddr=current_app.config['MAIL_FROM_ADDRESS'],
        toaddrs=current_app.config['SERVER_ADMIN_MAIL'],
        credentials=(current_app.config['MAIL_USERNAME'],
            current_app.config['MAIL_PASSWORD']),
        subject='Application Error'
    )
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
