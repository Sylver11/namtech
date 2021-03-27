from flask import jsonify, request
from flask_login import current_user
from application.extensions.security.models import User
import sys, traceback
import functools
import logging

LOG = logging.getLogger(__name__)

def catch_view_exception(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        post = False
        if request.method == 'POST':
            post = True
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            template = 'User uuid: {}\nTraceback: {}'
            user_uuid = 'Unkown'
            if isinstance(current_user, User):
                user_uuid = current_user.uuid
            admin_error_message = template.format(
                    user_uuid,
                    traceback.format_exc())
            LOG.error(admin_error_message)
            template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            user_error_message = template.format(type(ex).__name__, ex.args)
            if post:
                return jsonify(user_error_message), 500
            return user_error_message
    return inner
