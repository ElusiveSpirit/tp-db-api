from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import TextField, BooleanField, IntegerField, FieldList
from wtforms.validators import Required
from app.handlers import IncorrectRequest

from .models import Thread
from app.user.models import User
from app.forum.models import Forum


class ThreadForm(FlaskForm):
    title = TextField(validators=[Required()])
    message = TextField(validators=[Required()])
    slug = TextField(validators=[Required()])
    isClosed = BooleanField(false_values=[False])
    isDeleted = BooleanField(false_values=[False])
    date = TextField(validators=[Required()])
    user = TextField(validators=[Required()])
    forum = TextField(validators=[Required()])

    def save(self):
        user = User.query.filter_by(email=self.user.data).first_or_404()
        forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
        thread = Thread.query.filter_by(slug=self.slug.data).first()
        if thread:
            raise IncorrectRequest

        thread = Thread(
            title=self.title.data,
            message=self.message.data,
            slug=self.slug.data,
            isClosed=self.isClosed.data,
            isDeleted=self.isDeleted.data,
            date=self.date.data,
            user=user,
            forum=forum
        )
        thread.save()
        return thread


class ThreadDetailForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    related = FieldList(TextField(), max_entries=2)

    def get_thread_data(self):
        thread = Thread.query.get_or_404(self.thread.data)
        return thread.serialize(self.related.data)


class ThreadCloseForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def close(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isClosed = True
        thread.save()


class ThreadRemoveForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def remove(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isDeleted = True
        thread.save()
