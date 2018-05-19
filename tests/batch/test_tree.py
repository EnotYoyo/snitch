import pytest

from snitch.snark import snark
from snitch.config import config
from tests.utils import empty_database, send_json, app, bytes_to_base64, base64_to_bytes


def create_user(app, login, password, vk_id):
    prover = snark.Prover(config.PROVING_KEY)
    sk, pk = prover.get_key(login, password)
    response = send_json(app, "post", "/users", dict(login=login, vk_id=vk_id, hash=bytes_to_base64(pk)))
    assert response.get_json() == [{"id": 1, "login": login}, 201]
    return sk, pk


def test_get(empty_database, app):
    sk1, pk1 = create_user(app, "login", "pass", "1")
    response = app.get("/path", query_string=dict(user_hash=bytes_to_base64(pk1)))
    tree = snark.MerkleTree(config.TREE, config.TREE_INDEX)
    assert tree.get_path(pk1) == base64_to_bytes(response.get_json()["path"])
