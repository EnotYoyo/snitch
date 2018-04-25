from snitch import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(8192))
    reviews = db.relationship('Review', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name