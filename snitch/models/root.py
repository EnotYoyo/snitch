from snitch import db


class Root(db.Model):
    hash = db.Column(db.Binary, primary_key=True)

    def __repr__(self):
        return '<Root %r>' % self.hash