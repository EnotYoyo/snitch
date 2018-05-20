import functools
from io import BytesIO

import pytest

from snitch.config import config
from snitch import models
from tests.utils import empty_database, send_json, app


def test_product_url(empty_database, app):
    response = app.get("/products")
    assert response.get_json() == {"products": []}


@pytest.mark.parametrize("request", [
    dict(count=4),
    dict(offset=8),
    dict(category="other"),
    dict(count=15, offset=16),
    dict(count=23, category="books"),
    dict(offset=42, category="films"),
    dict(count=4, offset=8, category="other"),

])
def test_product_empty_list(empty_database, app, request):
    send = functools.partial(send_json, app, "get", "/products")

    response = send(request)
    assert response.get_json() == {"products": []}


def test_product_create(empty_database, app):
    send = functools.partial(send_json, app, "post", "/products")

    response = app.post("/products")
    assert response.get_json() == {"message": {"name": "Missing required parameter in the JSON body"}}

    response = send(dict(name="Product 1"))
    assert response.get_json() == {"message": {"description": "Missing required parameter in the JSON body"}}

    response = send(dict(name="Product 1", description="My test product"))
    assert response.get_json() == {"message": {"category": "Missing required parameter in the JSON body"}}

    response = send(dict(name="Product 1", description="My test product", category="other"))
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Product 1", "description": "My test product",
                                   "rate": 0, "image": config.DEFAULT_IMAGE_NAME, "reviews": 0}


def test_product_bad_category(empty_database, app):
    send = functools.partial(send_json, app, "post", "/products")

    response = send(dict(name="Product 1", description="My test product", category="4815162342"))
    assert response.status_code == 400


def test_create_not_unique(empty_database, app):
    send = functools.partial(send_json, app, "post", "/products")
    response = send(dict(name="Product 1", description="My test product", category="other"))
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Product 1", "description": "My test product",
                                   "rate": 0, "reviews": 0, "image": config.DEFAULT_IMAGE_NAME}

    response = send(dict(name="Product 1", description="My test product [2]", category="books"))
    assert response.status_code == 409


def test_product_list(empty_database, app):
    send = functools.partial(send_json, app, "post", "/products")
    products = [
        {"id": 1, "name": "Product 0", "description": "My test product [0]", "rate": 0, "reviews": 0,
         "image": config.DEFAULT_IMAGE_NAME},
        {"id": 2, "name": "Product 1", "description": "My test product [1]", "rate": 0, "reviews": 0,
         "image": config.DEFAULT_IMAGE_NAME},
        {"id": 3, "name": "Product 2", "description": "My test product [2]", "rate": 0, "reviews": 0,
         "image": config.DEFAULT_IMAGE_NAME},
        {"id": 4, "name": "Product 3", "description": "My test product [3]", "rate": 0, "reviews": 0,
         "image": config.DEFAULT_IMAGE_NAME}
    ]
    response = send(dict(name="Product 0", description="My test product [0]", category="other"))
    assert response.status_code == 201
    assert response.get_json() == products[0]

    response = send(dict(name="Product 1", description="My test product [1]", category="films"))
    assert response.status_code == 201
    assert response.get_json() == products[1]

    response = send(dict(name="Product 2", description="My test product [2]", category="books"))
    assert response.status_code == 201
    assert response.get_json() == products[2]

    response = send(dict(name="Product 3", description="My test product [3]", category="books"))
    assert response.status_code == 201
    assert response.get_json() == products[3]

    send_get = functools.partial(send_json, app, "get", "/products")

    response = app.get("/products")
    assert response.get_json() == {"products": products}

    response = send_get(dict(count=1))
    assert response.get_json() == {"products": products[:1]}

    response = send_get(dict(offset=1))
    assert response.get_json() == {"products": products[1:]}

    response = send_get(dict(count=1, offset=1))
    assert response.get_json() == {"products": products[1:2]}

    response = send_get(dict(count=1, offset=1, category="books"))
    assert response.get_json() == {"products": products[3:]}

    response = send_get(dict(count=10, category="films"))
    assert response.get_json() == {"products": products[1:2]}

    response = send_get(dict(category="books"))
    assert response.get_json() == {"products": products[2:]}

    response = send_get(dict(category="other"))
    assert response.get_json() == {"products": products[0:1]}


def test_reviews_len(empty_database, app):
    send = functools.partial(send_json, app, "post", "/products")
    response = send(dict(name="Product 1", description="My test product", category="other"))
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Product 1", "description": "My test product",
                                   "rate": 0, "image": config.DEFAULT_IMAGE_NAME, "reviews": 0}

    review = models.Review(id=b"4", product_id=1, review="Review [1] test_create!", rate=1)
    empty_database.session.add(review)

    review = models.Review(id=b"8", product_id=1, review="Review [2] test_create!", rate=2)
    empty_database.session.add(review)

    review = models.Review(id=b"15", product_id=1, review="Review [3] test_create!", rate=3)
    empty_database.session.add(review)

    review = models.Review(id=b"16", product_id=1, review="Review [4] test_create!", rate=4)
    empty_database.session.add(review)

    review = models.Review(id=b"23", product_id=1, review="Review [5] test_create!", rate=5)
    empty_database.session.add(review)

    review = models.Review(id=b"42", product_id=1, review="Review [6] test_create!", rate=5)
    empty_database.session.add(review)

    empty_database.session.commit()

    response = app.get("/products")
    assert response.status_code == 200
    response = response.get_json()["products"][0]
    assert response["name"] == "Product 1"
    assert response["description"] == "My test product"
    assert response["rate"] == 20 / 6
    assert response["reviews"] == 6
