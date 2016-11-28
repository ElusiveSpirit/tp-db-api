from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import TextField, BooleanField, TextAreaField, BooleanField, IntegerField, FieldList
from wtforms.validators import Required, AnyOf
from app.handlers import IncorrectRequest

from .models import Forum
from app.user.models import User, special_filter
from app.thread.models import Thread
from app.post.models import Post


class ForumForm(FlaskForm):
    user = TextField('email', validators=[Required()])
    short_name = TextField('short_name', validators=[Required()])
    name = TextField('name', validators=[Required()])

    def save(self):
        forum = Forum.query.filter(or_(
            Forum.name == self.name.data,
            Forum.short_name == self.short_name.data
        )).first()
        if forum:
            raise IncorrectRequest

        forum = Forum(
            name=self.name.data,
            short_name=self.short_name.data,
            user=User.query.filter_by(email=self.user.data).first_or_404()
        )
        forum.save()
        return forum


class ForumDetailForm(FlaskForm):
    forum = TextField('short_name', validators=[Required()])
    related = TextField('related')

    def get_forum_data(self):
        forum = Forum.query.filter_by(
            short_name=self.forum.data).first_or_404()
        return forum.serialize(related=[self.related.data])


class ForumThreadListForm(FlaskForm):
    forum = TextField(validators=[Required()])
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])
    related = FieldList(TextField(), max_entries=2)

    def get_thread_list_data(self):
        forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
        thread_list_qs = forum.threads

        return [t.serialize(self.related.data) for t in (magic_filter(thread_list_qs, self.data, Thread)).all()]


class ForumUserListForm(FlaskForm):
    forum = TextField(validators=[Required()])
    since_id = IntegerField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])

    def get_user_list_data(self):
        forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
        user_list_qs = forum.users

        return [t.serialize() for t in (special_filter(user_list_qs, self.data)).all()]


class ForumPostListForm(FlaskForm):
    forum = TextField(validators=[Required()])
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])
    related = FieldList(TextField(), max_entries=2)

    def get_post_list_data(self):
        forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
        post_list_qs = forum.posts.filter(Post.isDeleted==False)

        return [t.serialize(self.related.data) for t in (magic_filter(post_list_qs, self.data, Post)).all()]
