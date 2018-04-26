import functools
import json

import pytest

import snitch
from tests.utils import empty_database, send_json, app


def test_product_empty_list(empty_database, app):
    send = functools.partial(send_json, app, 'get', '/products')

    response = app.get('/products')
    assert response.get_json() == {"products": []}

    response = send(dict(count=100))
    assert response.get_json() == {"products": []}

    response = send(dict(offset=100))
    assert response.get_json() == {"products": []}

    response = send(dict(count=100, offset=100))
    assert response.get_json() == {"products": []}


def test_product_create(empty_database, app):
    send = functools.partial(send_json, app, 'post', '/products')

    response = app.post('/products')
    assert response.get_json() == {'message': {'name': 'Missing required parameter in the JSON body'}}

    response = send(dict(name="Product 1"))
    assert response.get_json() == {'message': {'description': 'Missing required parameter in the JSON body'}}

    response = send(dict(name="Product 1", description="My test product"))
    assert response.get_json() == [{'id': 1, 'name': "Product 1", 'description': "My test product"}, 201]


def create_not_unique(empty_database, app):
    send = functools.partial(send_json, app, 'post', '/products')
    response = send(dict(name="Product 1", description="My test product"))
    assert response.get_json() == [{'id': 1, 'name': "Product 1", 'description': "My test product"}, 201]

    response = send(dict(name="Product 1", description="My test product [2]"))
    assert response.get_json() == 409


def test_product_list(empty_database, app):
    send = functools.partial(send_json, app, 'post', '/products')
    products = [
        {'id': 1, 'name': "Product 0", 'description': "My test product [0]"},
        {'id': 2, 'name': "Product 1", 'description': "My test product [1]"},
        {'id': 3, 'name': "Product 2", 'description': "My test product [2]"}
    ]
    response = send(dict(name="Product 0", description="My test product [0]"))
    assert response.get_json() == [products[0], 201]

    response = send(dict(name="Product 1", description="My test product [1]"))
    assert response.get_json() == [products[1], 201]

    response = send(dict(name="Product 2", description="My test product [2]"))
    assert response.get_json() == [products[2], 201]

    send_get = functools.partial(send_json, app, 'get', '/products')

    response = app.get('/products')
    assert response.get_json() == {"products": products}

    response = send_get(dict(count=1))
    assert response.get_json() == {"products": products[:1]}

    response = send_get(dict(offset=1))
    assert response.get_json() == {"products": products[1:]}

    response = send_get(dict(count=1, offset=1))
    assert response.get_json() == {"products": products[1:2]}
