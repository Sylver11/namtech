# NamTech

### Development ###
#### Requirements ####
- Python >= 3.8
- MySQL Server >= 8
#### Set up ####
###### Execute commands ######
```shell
$ git clone git@github.com:Sylver11/namtech.git
$ cd namtech
$ python3 -m venv venv
$ source venv/bin/activate
$ python setup.py install
```

###### Set environement variables ######
```shell
$ export SQLALCHEMY_DATABASE_URI = <ConnString>
$ export SECRET_KEY = <SecretKey>
$ export FLASK_APP = application/__init__.py
$ export FLASK_ENV = development
$ export FLASK_DEBUG = True
$ export TEST_USER_EMAIL = <Email>
$ export TEST_USER_FIRSTNAME = <Firstname>
$ export TEST_USER_LASTNAME = <Lastname>
$ export TEST_USER_PASSWORD = <Password>
$ export SERVER_ADMIN = <AdminEmailAddress>
$ export SERVER_NAME = <Servername>
$ export MAIL_SERVER = <MailServer>
$ export MAIL_USERNAME = <Email>
$ export MAIL_PASSWORD = <AppPassword>
```
> Note: You can also define the variables inside a .env file

###### Now execute ######
```shell
$ flask run
```

:thumbsup:
