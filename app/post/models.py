from datetime import datetime

from app import db
from app.utils import Model
from app.handlers import IncorrectRequest
from config import DATETIME

from app.user.models import User
from app.forum.models import Forum
from app.thread.models import Thread


class Post(Model):
    """Post's model class"""
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.Text(), nullable=False)
    likes = db.Column(db.Integer(), default=0)
    dislikes = db.Column(db.Integer(), default=0)

    isApproved = db.Column(db.Boolean(), default=False)
    isHighlighted = db.Column(db.Boolean(), default=False)
    isEdited = db.Column(db.Boolean(), default=False)
    isSpam = db.Column(db.Boolean(), default=False)
    isDeleted = db.Column(db.Boolean(), default=False)

    date = db.Column(db.DateTime(), nullable=False)

    parent_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    forum_id = db.Column(db.Integer(), db.ForeignKey('forum.id'), nullable=False)
    thread_id = db.Column(db.Integer(), db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, message, user_id, forum_id, thread_id, date, parent_id=None, isApproved=False,
                 isHighlighted=False, isEdited=False, isSpam=False, isDeleted=False):
        self.message = message
        self.date = datetime.strptime(date, DATETIME)
        self.isApproved = isApproved
        self.isHighlighted = isHighlighted
        self.isEdited = isEdited
        self.isSpam = isSpam
        self.isDeleted = isDeleted

        self.parent_id = parent_id
        self.user_id = user_id
        self.forum_id = forum_id
        self.thread_id = thread_id

    def serialize(self, related=[]):
        return {
            'id': self.id,
            'date': self.date.strftime(DATETIME),
            'message': self.message,
            'dislikes': self.dislikes,
            'likes': self.likes,
            'points': self.likes - self.dislikes,
            'isApproved': self.isApproved,
            'isHighlighted': self.isHighlighted,
            'isEdited': self.isEdited,
            'isSpam': self.isSpam,
            'isDeleted': self.isDeleted,
            'user': self.user.serialize() if 'user' in related else self.user.email,
            'forum': self.forum.serialize() if 'forum' in related else self.forum.short_name,
            'thread': self.thread.serialize() if 'thread' in related else self.thread_id,
            'parent': self.parent_id
        }

    def __ref__(self):
        return '<Thread %s>' % self.id
