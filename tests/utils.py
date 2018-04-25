import pytest

from snitch import db


@pytest.yield_fixture
def empty_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
