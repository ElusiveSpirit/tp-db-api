from datetime import datetime

from app import db
from app.utils import Model
from config import DATETIME


class Thread(Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.String(40), unique=True, nullable=False)

    isClosed = db.Column(db.Boolean(), nullable=False)
    isDeleted = db.Column(db.Boolean(), nullable=False)

    date = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)

    def __init__(self, user, forum, title, message, slug, date, isClosed, isDeleted):
        self.title = title
        self.message = message
        self.slug = slug
        self.date = datetime.strptime(date, DATETIME)
        self.isClosed = isClosed
        self.isDeleted = isDeleted if isDeleted else False
        self.user_id = user.id
        self.forum_id = forum.id

    def serialize(self, related=[]):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'slug': self.slug,
            'isClosed': self.isClosed,
            'isDeleted': self.isDeleted,
            'date': self.date.strftime(DATETIME),
            'user': self.user.serialize() if 'user' in related else self.user.email,
            'forum': self.forum.serialize() if 'forum' in related else self.forum.short_name,
        }


    def __repr__(self):
        return '<Thread %s>' % self.slug
