from werkzeug.exceptions import Forbidden
import functools

def import_user():
    try:
        from flask_login import current_user
        return current_user
    except ImportError:
        raise ImportError(
            'User argument not passed and Flask-Login current_user could not be imported.')


def ability_required(ability, get_user=import_user):
    """
    Takes an ability (a string name of either a role or an ability) and returns the function if the user has that ability
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            from .models import Ability
            desired_ability = Ability.query.filter_by(name=ability).first()
            user_abilities = []
            current_user = get_user()
            for role in current_user.roles:
                user_abilities += role.abilities
            if desired_ability in user_abilities:
                return func(*args, **kwargs)
            else:
                raise Forbidden("You do not have access")
        return inner
    return wrapper


def role_required(role, get_user=import_user):
    """
    Takes an role (a string name of either a role or an ability) and returns the function if the user has that role
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            from .models import Role
            current_user = get_user()
            if role in current_user.roles:
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper
