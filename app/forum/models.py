from app import db
from app.utils import Model


class Forum(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True, nullable=False)
    short_name = db.Column(db.String(60), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # backref
    threads = db.relationship('Thread', backref='forum',  lazy='dynamic')

    def __init__(self, name, short_name, user):
        self.name = name
        self.short_name = short_name
        self.user_id = user.id

    def __repr__(self):
        return '<Forum %s>' % self.short_name

    def serialize(self, related=[]):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'user': self.user.serialize() if 'user' in related else self.user.email
        }
