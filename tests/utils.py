import base64
import json
import os

import pytest

import snitch
from snitch import db
from snitch.config import config


@pytest.yield_fixture
def empty_database():
    db.create_all()
    os.remove(config.TREE)
    os.remove(config.TREE_INDEX)
    yield db
    db.session.remove()
    db.drop_all()


@pytest.yield_fixture
def app():
    _app = snitch.app.test_client()
    yield _app


def send_json(app, method, endpoint, data=''):
    return getattr(app, method)(endpoint, data=json.dumps(data), content_type='application/json')


def bytes_to_base64(b):
    return base64.b64encode(b).decode('utf-8')


def base64_to_bytes(s):
    return base64.b64decode(s.encode('utf-8'))
