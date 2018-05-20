import pytest
import sqlalchemy

from snitch.config import config
from snitch.models import Product, Review

from tests.utils import empty_database


def test_connect(empty_database):
    product = Product.query.all()
    assert len(product) == 0


def test_create(empty_database):
    product = Product(name="Test product", description="description", category="category")
    empty_database.session.add(product)
    empty_database.session.commit()
    assert product.id == 1
    assert product.name == "Test product"
    assert product.description == "description"
    assert product.category == "category"


def test_russian_create(empty_database):
    product = Product(name="Тестовый product", description="description описание", category="категория")
    empty_database.session.add(product)
    empty_database.session.commit()
    assert product.id == 1
    assert product.name == "Тестовый product"
    assert product.description == "description описание"
    assert product.category == "категория"


def test_unique_name(empty_database):
    product1 = Product(name="Test product", description="description")
    product2 = Product(name="Test product", description="description")
    empty_database.session.add(product1)
    empty_database.session.add(product2)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_name(empty_database):
    product = Product()
    empty_database.session.add(product)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_autoincrement(empty_database):
    product1 = Product(name="Test product1", description="description")
    product2 = Product(name="Test product2", description="description")
    product3 = Product(name="Test product3", description="description")
    empty_database.session.add_all([product1, product2, product3])
    empty_database.session.commit()
    assert product1.id == 1
    assert product2.id == 2
    assert product3.id == 3


def test_reviews(empty_database):
    product1 = Product(name="Test product1", description="description")
    review1 = Review(id=b"1", product_id=1, review="Review 1!", rate=1)
    review2 = Review(id=b"2", product_id=1, review="Review 2!", rate=4)
    empty_database.session.add_all([product1, review1, review2])
    empty_database.session.commit()
    reviews = product1.reviews
    assert reviews[0].id == b"1"
    assert reviews[0].review == "Review 1!"
    assert reviews[1].id == b"2"
    assert reviews[1].review == "Review 2!"
    assert product1.rate == 2.5


def test_serialise(empty_database):
    product = Product(name="Test product", description="description")
    empty_database.session.add(product)
    empty_database.session.commit()
    assert product.serialize == {"id": 1, "name": "Test product", "image": config.DEFAULT_IMAGE,
                                 "description": "description", "rate": 0}
