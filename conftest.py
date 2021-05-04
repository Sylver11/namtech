import os
import pytest
from application import create_app
from application.database import db


@pytest.fixture()
def app():
    app = create_app('Testing')
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def script_info(app):
    from flask.cli import ScriptInfo
    return ScriptInfo(create_app=lambda info: app)
