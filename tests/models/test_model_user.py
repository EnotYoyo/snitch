import pytest
import sqlalchemy
from snitch.models import User

from tests.utils import empty_database


def test_connect(empty_database):
    product = User.query.all()
    assert len(product) == 0


def test_create(empty_database):
    user = User(login="login test_create", hash="hash test_create")
    empty_database.session.add(user)
    empty_database.session.commit()
    assert user.id == 1
    assert user.login == "login test_create"
    assert user.hash == "hash test_create"


def test_russian_create(empty_database):
    user = User(login="логин from russia", hash="hash test_create")
    empty_database.session.add(user)
    empty_database.session.commit()
    assert user.id == 1
    assert user.login == "логин from russia"
    assert user.hash == "hash test_create"


def test_unique_login(empty_database):
    user1 = User(login="login test_unique_login", hash="hash1")
    user2 = User(login="login test_unique_login", hash="hash2")
    empty_database.session.add_all([user1, user2])
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_login(empty_database):
    user = User(hash="hash")
    empty_database.session.add(user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_hash(empty_database):
    user = User(login="login test_nullable_hash")
    empty_database.session.add(user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_autoincrement(empty_database):
    user1 = User(login="login test_autoincrement1", hash="hash1")
    user2 = User(login="login test_autoincrement2", hash="hash2")
    user3 = User(login="login test_autoincrement3", hash="hash2")
    empty_database.session.add_all([user1, user2, user3])
    empty_database.session.commit()
    assert user1.id == 1
    assert user2.id == 2
    assert user3.id == 3
