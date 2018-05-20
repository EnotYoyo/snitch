from decimal import Decimal

from sqlalchemy import func

from snitch import db, app
from snitch import models


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(8192))
    category = db.Column(db.String(9))
    image = db.Column(db.String(41))
    reviews = db.relationship('Review', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image or app.config["DEFAULT_IMAGE_NAME"],
            'description': self.description,
            'rate': self.rate or 0,
            'reviews': len(self.reviews)
        }

    @property
    def rate(self):
        r = db.session.query(func.avg(models.Review.rate)).filter(models.Review.product_id == self.id).first()[0]
        if r is not None:
            r = float(r)
        return r
