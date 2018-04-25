from snitch import db


class Root(db.Model):
    hash = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        return '<Root %r>' % self.hash