from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import Required, Length, AnyOf

from app.thread.models import magic_filter


def get_user_form(data):
    if 'isAnonymous' in data and data['isAnonymous']:
        return AnonymousUserForm(data=data)
    else:
        return UserForm(data=data)


class UserForm(FlaskForm):
    email = TextField('email', validators=[Required()])
    username = TextField('username', validators=[Required()])
    name = TextField('name', validators=[Required()])
    about = TextAreaField('about', validators=[Required()])
    isAnonymous = BooleanField('isAnonymous', false_values=[False])


class UpdateUserForm(FlaskForm):
    user = TextField('email', validators=[Required()])
    name = TextField('name', validators=[Required()])
    about = TextAreaField('about', validators=[Required()])


class AnonymousUserForm(FlaskForm):
    email = TextField('email', validators=[Required()])
    username = TextField('username')
    name = TextField('name')
    about = TextAreaField('about')
    isAnonymous = BooleanField('isAnonymous', false_values=[False])


class FollowForm(FlaskForm):
    follower = TextField('follower', validators=[Required()])
    followee = TextField('followee', validators=[Required()])


class UserPostListForm(FlaskForm):
    user = TextField(validators=[Required()])
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])

    def get_post_list_data(self):
        user = User.query.filter_by(email=self.user.data).first_or_404()
        post_list_qs = user.posts

        return [t.serialize() for t in (magic_filter(post_list_qs, self.data)).all()]

