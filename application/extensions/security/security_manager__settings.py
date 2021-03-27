class SecurityManager__Settings(object):

    USER_ENABLE_REGISTER = True
    USER_SET_DB_DEFAULTS = True
    USER_DEFAULT_ROLE_NAME = 'user'
    USER_DEFAULT_ROLE_DESCRIPTION = 'Normal User'
    USER_TEST_URL = '/security/test'
    USER_LOGIN_URL = '/login'
    USER_LOGOUT_URL = '/logout'
    USER_REGISTER_URL = '/register'
    USER_LOGIN_TEMPLATE = 'security/login.html' #:
    USER_REGISTER_TEMPLATE = 'security/register.html' #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'security/forgot_password.html' #:
    USER_CONFIRM_EMAIL_TEMPLATE = 'security/emails/confirm_email' #:
    USER_AFTER_LOGOUT_URL = '/'
