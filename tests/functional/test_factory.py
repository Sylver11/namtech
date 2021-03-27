from application import create_app
import os

def test_config():
    assert not create_app().testing
    assert create_app('testing').testing


def test_user_route(client):
    response = client.get('/security/test')
    assert response.data == b'Success'


def test_admin_route(client):
    response = client.get('/admin/test')
    assert response.data == b'Success'

