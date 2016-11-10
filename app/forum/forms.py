from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import TextField, BooleanField, TextAreaField, BooleanField
from wtforms.validators import Required
from app.handlers import IncorrectRequest

from .models import Forum
from app.user.models import User


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
        return forum.serialize(less=(self.related.data != 'user'))
