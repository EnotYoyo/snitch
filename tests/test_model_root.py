from snitch.models import Root
from .utils import empty_database


def test_connect(empty_database):
    review = Root.query.all()
    assert len(review) == 0


def test_create(empty_database):
    root = Root(hash="very long hash")
    empty_database.session.add(root)
    empty_database.session.commit()
    assert root.hash == "very long hash"
