from snitch.models import Root
from tests.utils import empty_database


def test_connect(empty_database):
    review = Root.query.all()
    assert len(review) == 0


def test_create(empty_database):
    root = Root(hash=b"very long hash")
    empty_database.session.add(root)
    empty_database.session.commit()
    assert root.hash == b"very long hash"
