import datetime
import functools
import json
import os
import random
from unittest import mock
from unittest.mock import patch

import pytest

import snitch
from snitch.config import config
from snitch.snark import snark
from tests.utils import send_json, app, bytes_to_base64, create_user, base64_to_bytes


@pytest.yield_fixture
def empty_database():
    f = open(config.TREE, "w")
    f.close()
    f = open(config.TREE_INDEX, "w")
    f.close()

    snitch.db.drop_all()
    snitch.db.create_all()
    p1 = snitch.models.Product(name="test product 1", description="desc 1")
    p2 = snitch.models.Product(name="test product 2", description="desc 2")
    snitch.db.session.add_all([p1, p2])
    snitch.db.session.commit()
    yield snitch.db
    snitch.db.session.remove()
    snitch.db.drop_all()


def create_review(product_id, review, sk, tree_path):
    review_struct = {
        'review': review,
        'nonce': random.randint(0, 100500)
    }

    review = json.dumps(review_struct)
    prover = snark.Prover(config.PROVING_KEY)
    zk_snark, review_id, review_sig, root = prover.create_snark(sk, tree_path, product_id, review)
    review = {
        'review': review,
        'review_id': bytes_to_base64(review_id),
        'review_sig': bytes_to_base64(review_sig),
        'product_id': product_id,
        'snark': bytes_to_base64(zk_snark),
        'tree_root': bytes_to_base64(root)
    }
    print(root)
    return review


def test_review_empty_list(empty_database, app):
    send = functools.partial(send_json, app, "get", "/reviews")

    response = send(dict(product_id=1))
    assert response.get_json() == {"reviews": []}

    response = send(dict(product_id=1, count=100))
    assert response.get_json() == {"reviews": []}

    response = send(dict(product_id=2, offset=100))
    assert response.get_json() == {"reviews": []}

    response = send(dict(product_id=20, count=100, offset=100))
    assert response.get_json() == {"reviews": []}


def test_review_create(empty_database, app):
    send = functools.partial(send_json, app, "post", "/reviews")

    response = app.post("/reviews")
    assert response.get_json() == {"message": {"product_id": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1))
    assert response.get_json() == {"message": {"review": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1, review="4 8 15"))
    assert response.get_json() == {"message": {"review_id": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1, review="4 8 15", review_id="1"))
    assert response.get_json() == {"message": {"review_sig": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1, review="4 8 15", review_id="1", review_sig="1"))
    assert response.get_json() == {"message": {"snark": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1, review="4 8 15", review_id="1", review_sig="1", snark="1"))
    assert response.get_json() == {"message": {"tree_root": "Missing required parameter in the JSON body"}}

    response = send(dict(product_id=1, review="4 8 15", review_id="1", review_sig="1", tree_root="1"))
    assert response.get_json() == {"message": {"snark": "Missing required parameter in the JSON body"}}

    tree = snark.MerkleTree(config.TREE, config.TREE_INDEX)
    sk, pk = create_user(app, "login", "pass", 1)
    response = app.get("/path", query_string=dict(user_hash=bytes_to_base64(pk)))
    review = create_review("1", "4 8 1 16 23 42", sk, base64_to_bytes(response.get_json()["path"]))
    d = datetime.datetime.utcnow()
    with mock.patch("datetime.datetime") as patched:
        patched.utcnow = mock.Mock(return_value=d)
        response = send(review)
        assert response.get_json() == [
            {"id": review["review_id"], "review": "4 8 1 16 23 42", "created_time": int(d.timestamp())}, 201]


# @patch("snitch.snark.snark.Verifier")
# @patch("snitch.models.root.Root")
# def test_product_list(verifier, root, empty_database, app):
#     root = mock.Mock()
#     root.return_value.query.return_value.filter.return_value.first = True
#     verifier.return_value.verify_snark = mock.Mock(return_value=(True, "Patched!"))
#
#     send = functools.partial(send_json, app, "post", "/reviews")
#     review = [
#         {"id": bytes_to_base64(b"8"), "review": "My test review [0]"},
#         {"id": bytes_to_base64(b"4"), "review": "My test review [1]"},
#         {"id": bytes_to_base64(b"42"), "review": "My test review [2]"}
#     ]
#
#     review_1 = {
#         'review': """{
#             \"review\": \"My test review [0]\",
#             \"nonce\": 4
#         }""",
#         'review_id': bytes_to_base64(b"8"),
#         'review_sig': bytes_to_base64(b"15"),
#         'product_id': "1",
#         'snark': bytes_to_base64(b"16"),
#         'tree_root': bytes_to_base64(b"23")
#     }
#
#     review_2 = {
#         'review': """{
#             \"review\": \"My test review [1]\",
#             \"nonce\": 42
#         }""",
#         'review_id': bytes_to_base64(b"4"),
#         'review_sig': bytes_to_base64(b"8"),
#         'product_id': "1",
#         'snark': bytes_to_base64(b"15"),
#         'tree_root': bytes_to_base64(b"16")
#     }
#
#     review_3 = {
#         'review': """{
#             \"review\": \"My test review [2]\",
#             \"nonce\": 23
#         }""",
#         'review_id': bytes_to_base64(b"42"),
#         'review_sig': bytes_to_base64(b"4"),
#         'product_id': "2",
#         'snark': bytes_to_base64(b"8"),
#         'tree_root': bytes_to_base64(b"15")
#     }
#
#     response = send(review_1)
#     json_data = response.get_json()
#     assert "created_time" in json_data[0]
#
#     del json_data[0]["created_time"]
#     assert response.get_json() == [review[0], 201]
#
#     response = send(review_2)
#     json_data = response.get_json()
#     assert "created_time" in json_data[0]
#
#     del json_data[0]["created_time"]
#     assert response.get_json() == [review[1], 201]
#
#     response = send(review_3)
#     json_data = response.get_json()
#     assert "created_time" in json_data[0]
#
#     del json_data[0]["created_time"]
#     assert response.get_json() == [review[2], 201]
#
#     send_get = functools.partial(send_json, app, "get", "/reviews")
#
#     response = send_get(dict(product_id=1, count=1))
#     json_data = response.get_json()
#
#     for r in json_data["reviews"]:
#         del r["created_time"]
#     assert json_data == {"reviews": review[:1]}
#
#     response = send_get(dict(product_id=1, offset=1))
#     json_data = response.get_json()
#
#     for r in json_data["reviews"]:
#         del r["created_time"]
#     assert json_data == {"reviews": review[1:2]}
#
#     response = send_get(dict(product_id=2, count=1))
#     json_data = response.get_json()
#
#     for r in json_data["reviews"]:
#         del r["created_time"]
#     assert json_data == {"reviews": review[2:]}
