from snitch import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), nullable=False, unique=True)
    hash = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login