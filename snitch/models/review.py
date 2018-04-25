import datetime

from snitch import db
from snitch.models.product import Product


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    review = db.Column(db.String(8192), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Review %r>' % self.id
