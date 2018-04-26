import datetime
import functools
import json
from unittest import mock

import pytest

import snitch
from tests.utils import send_json, app


@pytest.yield_fixture
def empty_database():
    snitch.db.create_all()
    p1 = snitch.models.Product(name="test product 1", description="desc 1")
    p2 = snitch.models.Product(name="test product 2", description="desc 2")
    snitch.db.session.add_all([p1, p2])
    snitch.db.session.commit()
    yield snitch.db
    snitch.db.session.remove()
    snitch.db.drop_all()


def test_review_empty_list(empty_database, app):
    send = functools.partial(send_json, app, 'get', '/reviews')

    response = app.get('/reviews')
    assert response.get_json() == {"reviews": []}

    response = send(dict(count=100))
    assert response.get_json() == {"reviews": []}

    response = send(dict(offset=100))
    assert response.get_json() == {"reviews": []}

    response = send(dict(count=100, offset=100))
    assert response.get_json() == {"reviews": []}


def test_review_create(empty_database, app):
    send = functools.partial(send_json, app, 'post', '/reviews')

    response = app.post('/reviews')
    assert response.get_json() == {'message': {'product_id': 'Missing required parameter in the JSON body'}}

    response = send(dict(product_id=1))
    assert response.get_json() == {'message': {'review': 'Missing required parameter in the JSON body'}}

    d = datetime.datetime.utcnow()
    with mock.patch('datetime.datetime') as patched:
        patched.utcnow = mock.Mock(return_value=d)
        response = send(dict(product_id=1, review="My test review"))
        assert response.get_json() == [{'id': 1, 'review': "My test review", "created_time": int(d.timestamp())}, 201]


def test_product_list(empty_database, app):
    d = datetime.datetime.utcnow()
    with mock.patch('datetime.datetime') as patched:
        patched.utcnow = mock.Mock(return_value=d)
        timestamp = int(d.timestamp())

        send = functools.partial(send_json, app, 'post', '/reviews')
        review = [
            {'id': 1, 'review': "My test review [0]", "created_time": timestamp},
            {'id': 2, 'review': "My test review [1]", "created_time": timestamp},
            {'id': 3, 'review': "My test review [2]", "created_time": timestamp}
        ]

        response = send(dict(product_id=1, review=review[0]["review"]))
        assert response.get_json() == [review[0], 201]

        response = send(dict(product_id=1, review=review[1]["review"]))
        assert response.get_json() == [review[1], 201]

        response = send(dict(product_id=2, review=review[2]["review"]))
        assert response.get_json() == [review[2], 201]

        send_get = functools.partial(send_json, app, 'get', '/reviews')

        response = app.get('/reviews')
        assert response.get_json() == {"reviews": review}

        response = send_get(dict(count=1))
        assert response.get_json() == {"reviews": review[:1]}

        response = send_get(dict(offset=1))
        assert response.get_json() == {"reviews": review[1:]}

        response = send_get(dict(count=1, offset=1))
        assert response.get_json() == {"reviews": review[1:2]}
