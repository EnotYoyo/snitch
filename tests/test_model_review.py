import datetime

import pytest
import sqlalchemy
from snitch import db
from snitch.models import Review, Product


@pytest.yield_fixture
def empty_database():
    db.create_all()
    p1 = Product(name="test product 1", description="desc 1")
    p2 = Product(name="test product 2", description="desc 2")
    db.session.add_all([p1, p2])
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()


def test_connect(empty_database):
    review = Review.query.all()
    assert len(review) == 0


def test_create(empty_database):
    review = Review(product_id=1, review="Review test_create!")
    empty_database.session.add(review)
    empty_database.session.commit()
    assert review.id == 1
    assert review.product_id == 1
    assert review.review == "Review test_create!"
    assert isinstance(review.created_time, datetime.datetime)


def test_russian_create(empty_database):
    review = Review(product_id=1, review="Комментарий о продукте from Russia")
    empty_database.session.add(review)
    empty_database.session.commit()
    assert review.id == 1
    assert review.product_id == 1
    assert review.review == "Комментарий о продукте from Russia"
    assert isinstance(review.created_time, datetime.datetime)


def test_nullable_product_id(empty_database):
    review = Review(review="Review test_nullable_product_id")
    empty_database.session.add(review)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_review(empty_database):
    review = Review(product_id=1)
    empty_database.session.add(review)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_autoincrement(empty_database):
    review1 = Review(product_id=1, review="Review test_autoincrement1!")
    review2 = Review(product_id=1, review="Review test_autoincrement2!")
    review3 = Review(product_id=2, review="Review test_autoincrement3!")
    empty_database.session.add_all([review1, review2, review3])
    empty_database.session.commit()
    assert review1.id == 1
    assert review2.id == 2
    assert review3.id == 3
