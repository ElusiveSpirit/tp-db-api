from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import TextField, BooleanField, IntegerField, FieldList, ValidationError
from wtforms.validators import Required, AnyOf
from app.handlers import IncorrectRequest

from .models import Thread, magic_filter
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


class ThreadListForm(FlaskForm):
    user = TextField()
    forum = TextField()
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])

    def validate_user(self, field):
        # if both with data or not
        if (field.data and self.forum.data) or (not field.data and not self.forum.data):
            raise ValidationError

    def get_thread_list_data(self):
        if self.user.data:
            user = User.query.filter_by(email=self.user.data).first_or_404()
            thread_list_qs = user.threads
        else:
            forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
            thread_list_qs = forum.threads

        return [t.serialize() for t in (magic_filter(thread_list_qs, self.data)).all()]


class ThreadDetailForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    related = FieldList(TextField(), max_entries=2)

    def get_thread_data(self):
        thread = Thread.query.get_or_404(self.thread.data)
        return thread.serialize(self.related.data)


class ThreadOpenForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def open(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isClosed = False
        thread.save()


class ThreadCloseForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def close(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isClosed = True
        thread.save()


class ThreadSubscribeForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    user = TextField(validators=[Required()])

    def subscribe(self):
        user = User.query.filter_by(user=self.user.data).first_or_404()
        thread = Thread.query.get_or_404(self.thread.data)
        if user.subscribing.query.filter(thread.id).first():
            raise IncorrectRequest
        user.subscribing.append(thread)
        user.save()

    def unsubscribe(self):
        user = User.query.filter_by(user=self.user.data).first_or_404()
        thread = Thread.query.get_or_404(self.thread.data)
        if not user.subscribing.query.filter(thread.id).first():
            raise IncorrectRequest
        user.subscribing.remove(thread)
        user.save()


class ThreadRestoreForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def restore(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isDeleted = False
        thread.save()


class ThreadRemoveForm(FlaskForm):
    thread = IntegerField(validators=[Required()])

    def remove(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.isDeleted = True
        thread.save()
