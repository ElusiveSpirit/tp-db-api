from app import db
from app.utils import Model
from app.handlers import UserExists
from sqlalchemy.orm import aliased


user_followings = db.Table('user_followings', db.metadata,
    # Кто
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    # Кого
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Index('ix_user_followings', 'follower_id', 'following_id', unique=True),
)


class User(Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    username = db.Column(db.String(40))
    name = db.Column(db.String(40))
    about = db.Column(db.Text)

    isAnonymous = db.Column(db.Boolean, default=False)

    following = db.relationship('User', secondary=user_followings,
        primaryjoin=id==user_followings.c.follower_id,
        secondaryjoin=id==user_followings.c.following_id,
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, email, username, name, about, isAnonymous=False):
        self.email = email
        self.username = username
        self.name = name
        self.about = about
        self.isAnonymous = isAnonymous

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self, less=False):
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'about': self.about,
            'isAnonymous': self.isAnonymous
        }
        if not less:
            data['followers'] = [f.email for f in self.followers]
            data['following'] = [f.email for f in self.following]
        return data

    def create(self):
        if User.query.filter_by(email=self.email).first():
            raise UserExists
        return super(User, self).create()
