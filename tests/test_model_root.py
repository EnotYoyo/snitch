import datetime

import pytest
import sqlalchemy
from snitch import db
from snitch.models import Root


@pytest.yield_fixture
def empty_database():
    db.create_all()
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()


def test_connect(empty_database):
    review = Root.query.all()
    assert len(review) == 0


def test_create(empty_database):
    root = Root(hash="very long hash")
    empty_database.session.add(root)
    empty_database.session.commit()
    assert root.hash == "very long hash"
