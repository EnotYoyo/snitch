import base64

import pytest
import functools

from snitch.snark import snark
from tests.utils import empty_database, send_json, app


def create_users_keys():
    prover = snark.Prover('pk.key')
    sk1, pk1 = prover.get_key('user1', 'pass1')
    return sk1, pk1


def test_user_register(empty_database, app):
    send = functools.partial(send_json, app, "post", "/users")

    response = app.post("/users")
    assert response.get_json() == {"message": {"login": "Missing required parameter in the JSON body"}}

    response = send(dict(login="login1"))
    assert response.get_json() == {"message": {"vk_id": "Missing required parameter in the JSON body"}}

    response = send(dict(login="login", vk_id="1"))
    assert response.get_json() == {"message": {"hash": "Missing required parameter in the JSON body"}}

    sk, pk = create_users_keys()
    response = send(dict(login="login", vk_id="1", hash=base64.b64encode(pk).decode('utf-8')))
    assert response.get_json() == [{"id": 1, "login": "login"}, 201]


def test_create_not_unique_login(empty_database, app):
    pk1, pk2 = create_users_keys()

    send = functools.partial(send_json, app, "post", "/users")
    response = send(dict(login="login", vk_id="1", hash=base64.b64encode(pk1).decode('utf-8')))
    assert response.get_json() == [{"id": 1, "login": "login"}, 201]

    response = send(dict(login="login", vk_id="2", hash=base64.b64encode(pk2).decode('utf-8')))
    assert response.status_code == 409


def test_create_not_unique_vk_id(empty_database, app):
    pk1, pk2 = create_users_keys()

    send = functools.partial(send_json, app, "post", "/users")
    response = send(dict(login="login1", vk_id="1", hash=base64.b64encode(pk1).decode('utf-8')))
    assert response.get_json() == [{"id": 1, "login": "login1"}, 201]

    response = send(dict(login="login2", vk_id="1", hash=base64.b64encode(pk2).decode('utf-8')))
    assert response.status_code == 409


def test_create_not_unique_hash(empty_database, app):
    sk, pk = create_users_keys()

    send = functools.partial(send_json, app, "post", "/users")
    response = send(dict(login="login1", vk_id="1", hash=base64.b64encode(pk).decode('utf-8')))
    assert response.get_json() == [{"id": 1, "login": "login1"}, 201]

    response = send(dict(login="login2", vk_id="2", hash=base64.b64encode(pk).decode('utf-8')))
    assert response.status_code == 409