import base64
import datetime

from sqlalchemy import and_

from snitch import db
from snitch.models.product import Product


class Review(db.Model):
    id = db.Column(db.Binary, primary_key=True, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    rate = db.Column(db.Integer, nullable=False, default=0)
    review = db.Column(db.String(8192), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint(and_(0 < rate, rate < 5), name='check_rate'),
        {})

    def __repr__(self):
        return '<Review %r>' % self.id

    @property
    def serialize(self):
        return {
            'id': base64.b64encode(self.id).decode('utf-8'),
            'review': self.review,
            'created_time': int(self.created_time.timestamp())
        }
