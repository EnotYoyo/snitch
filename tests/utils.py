import json

import pytest

import snitch
from snitch import db


@pytest.yield_fixture
def empty_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.yield_fixture
def app():
    _app = snitch.app.test_client()
    yield _app


def send_json(app, method, endpoint, data=''):
    return getattr(app, method)(endpoint, data=json.dumps(data), content_type='application/json')
