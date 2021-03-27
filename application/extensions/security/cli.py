from .security_manager import SecurityManager
from .models import User, Group
from flask.cli import AppGroup
import click


security_cli = AppGroup('security')


@security_cli.command('get', help='email')
@click.argument('email')
def get_user_cli(email=None):
    pass

@security_cli.command('add-group')
@click.option('--group_name', prompt='Group Name',required=True)
@click.option('--admin_user_email', prompt='Admin User Email',required=True)
def add_group_cli(group_name, admin_user_email):
    user = User.query.filter_by(email=admin_user_email).first()
    if not user:
        click.echo('Failed: User does not exist.')
        return None
    if user.group:
        click.echo('Failed: User already part of another group')
        return None
    if user.group_admin:
        click.echo('Failed: User already admin of another group')
        return None
    group = Group(name=group_name)
    security_manager = SecurityManager()
    group = security_manager.add_group(group)
    if isinstance(group, Group):
        if group.uuid:
            user.group_uuid = group.uuid
            user.group_admin = True
            if not security_manager.update_user(user):
                click.echo('Failed: Could not update user details')
                return None
            click.echo('Success: Group successfully created')
            return None
        else:
            click.echo('Failed: Unkown reason')
            return None
    else:
        click.echo('Failed: Group name already in use.')
        return None
    return None

@security_cli.command('add-user',)
@click.option('--firstname', prompt='Firstname',required=True)
@click.option('--secondname', prompt='Secondname',required=True)
@click.option('--email', prompt='Email',required=True)
@click.password_option(required=True)
@click.option('--group',
        prompt='Group name (optional)',
        default='None',
        help='Leave empty for default')
def add_user_cli(firstname, secondname, email, password, group):
    user = User(
            firstname=firstname,
            secondname=secondname,
            email=email)
    user.set_password(password)
    security_manager = SecurityManager()
    if group != 'None':
        group = security_manager.get_group_by_name(group)
        if not group:
            click.echo('Failed: The specified group does not exist')
            return None
        user.group = group
    user = security_manager.add_user(user)
    if isinstance(user, User):
        if user.uuid:
            feedback = 'Success: User created'
            if user.group:
                feedback += ' and added to ' + user.group.name + ' group.'
            click.echo(feedback)
            return None
        else:
            click.echo('Failed: Unknown reason')
            return None
    else:
        click.echo('Failed: User already exists')
    return None

@security_cli.command('update', help='fname, sname, email, pass and role')
@click.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('user_details', nargs=-1, type=click.UNPROCESSED)
def update_user_cli(user_details):
    pass

@security_cli.command('delete', help='email')
@click.argument('email')
def delete_user_cli(email):
    pass

