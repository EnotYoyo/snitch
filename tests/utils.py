import base64
import json
import os

import pytest

import snitch
from snitch import db
from snitch.config import config
from snitch.snark import snark


@pytest.yield_fixture
def empty_database():
    db.drop_all()
    db.create_all()
    f = open(config.TREE, "w")
    f.close()
    f = open(config.TREE_INDEX, "w")
    f.close()
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


def create_user(app, login, password, vk_id):
    prover = snark.Prover(config.PROVING_KEY)
    sk, pk = prover.get_key(login, password)
    response = send_json(app, "post", "/users", dict(login=login, vk_id=vk_id, hash=bytes_to_base64(pk)))
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "login": login}
    return sk, pk
