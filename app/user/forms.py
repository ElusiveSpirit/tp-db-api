from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField, BooleanField
from wtforms.validators import Required, Length


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
