from app import db


user_followings = db.Table('user_followings',
    # Кто
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    # Кого
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Index('ix_user_followings', 'follower_id', 'following_id', unique=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    username = db.Column(db.String(40))
    name = db.Column(db.String(40))
    about = db.Column(db.Text)

    isAnonymous = db.Column(db.Boolean, default=False)

    following = db.relationship('User', secondary=user_followings,
        backref=db.backref('pages', lazy='dynamic'))

    def __init__(self, email, username, name, about, isAnonymous=False):
        self.email = email
        self.username = username
        self.name = name
        self.about = about
        self.isAnonymous = isAnonymous

    def __repr__(self):
        return '<User %r>' % self.email
