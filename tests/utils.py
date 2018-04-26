import json

import pytest

from snitch import db


@pytest.yield_fixture
def empty_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


def send_json(app, method, endpoint, data=''):
    return getattr(app, method)(endpoint, data=json.dumps(data), content_type='application/json')
