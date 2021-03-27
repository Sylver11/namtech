from sqlalchemy.exc import IntegrityError
from application.extensions.security.security_manager import SecurityManager
from application.extensions.security.models import User, Role, Group
from application.database import db
import pytest
import uuid

def test_creating_new_user(app):
    """ Test to determine if user is successfully added to database """
    new_user = User(firstname = 'Justus',
            secondname = 'Voigt',
            email = 'connectmaeuse@gmail.com')
    new_user.set_password('SuperSecret')
    with app.app_context():
        security_manager = SecurityManager()
        new_user = security_manager.add_user(new_user)
        added_user = User.query.filter_by(uuid = new_user.uuid).first()
        assert isinstance(added_user, User)
        uuid_obj = uuid.UUID(str(added_user.uuid), version=4)
        assert str(uuid_obj) == str(added_user.uuid)
        assert added_user.firstname == 'Justus'
        assert added_user.secondname == 'Voigt'
        assert added_user.email == 'connectmaeuse@gmail.com'
        assert added_user.check_password('SuperSecret')
        assert added_user.thirdparty_authenticated == False
        assert not added_user.thirdparty_name
        assert not added_user.authenticated
        """ Checking if adding the same user fails due to unique constrain"""
        duplicate_user = User(firstname = 'Justus',
                secondname = 'Voigt',
                email = 'connectmaeuse@gmail.com',)
        db.session.add(duplicate_user)
        with pytest.raises(IntegrityError):
            db.session.commit()
