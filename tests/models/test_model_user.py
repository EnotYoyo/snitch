import pytest
import sqlalchemy
from snitch.models import User

from tests.utils import empty_database


def test_connect(empty_database):
    users = User.query.all()
    assert len(users) == 0


def test_create(empty_database):
    user = User(login="login test_create", vk_id=43, hash="hash test_create")
    empty_database.session.add(user)
    empty_database.session.commit()
    assert user.id == 1
    assert user.vk_id == 43
    assert user.login == "login test_create"
    assert user.hash == "hash test_create"


def test_russian_create(empty_database):
    user = User(login="логин from russia", vk_id=43, hash="hash test_create")
    empty_database.session.add(user)
    empty_database.session.commit()
    assert user.id == 1
    assert user.vk_id == 43
    assert user.login == "логин from russia"
    assert user.hash == "hash test_create"


def test_unique_login(empty_database):
    user1 = User(login="login test_unique_login", vk_id=23, hash="hash1")
    user2 = User(login="login test_unique_login", vk_id=43, hash="hash2")
    empty_database.session.add_all([user1, user2])
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_unique_vk_id(empty_database):
    user1 = User(login="test_unique_vk_id1", vk_id=43, hash="hash1")
    user2 = User(login="test_unique_vk_id2", vk_id=43, hash="hash2")
    empty_database.session.add_all([user1, user2])
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_login(empty_database):
    user = User(vk_id=43, hash="hash")
    empty_database.session.add(user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_hash(empty_database):
    user = User(login="login test_nullable_hash", vk_id=43)
    empty_database.session.add(user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_nullable_vk_id(empty_database):
    user = User(login="login test_nullable_hash", hash="hash")
    empty_database.session.add(user)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        empty_database.session.commit()


def test_autoincrement(empty_database):
    user1 = User(login="login test_autoincrement1", vk_id=4, hash="hash1")
    user2 = User(login="login test_autoincrement2", vk_id=8, hash="hash2")
    user3 = User(login="login test_autoincrement3", vk_id=15, hash="hash2")
    empty_database.session.add_all([user1, user2, user3])
    empty_database.session.commit()
    assert user1.id == 1
    assert user2.id == 2
    assert user3.id == 3
