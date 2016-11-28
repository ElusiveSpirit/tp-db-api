from datetime import datetime
from config import DATETIME
from app import db
from flask_wtf import FlaskForm
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from wtforms import TextField, BooleanField, IntegerField, FieldList, ValidationError
from wtforms.validators import Required, AnyOf
from app.handlers import IncorrectRequest

from .models import Thread, magic_filter
from app.user.models import User
from app.forum.models import Forum
from app.post.models import Post


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

        return [t.serialize() for t in (magic_filter(thread_list_qs, self.data, Thread)).all()]


class ThreadVoteForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    vote = IntegerField(validators=[AnyOf([1, -1])])

    def vote(self):
        thread = Thread.query.get_or_404(self.thread.data)
        if self.vote.data == 1:
            thread.likes += 1
        else:
            thread.dislikes += 1
        return thread.serialize()


class ThreadUpdateForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    message = TextField(validators=[Required()])
    slug = TextField(validators=[Required()])

    def update(self):
        thread = Thread.query.get_or_404(self.thread.data)
        thread.message = self.message.data
        thread.slug = self.slug.data
        thread.save()
        return thread.serialize()


class ThreadDetailForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    related = FieldList(TextField(validators=[AnyOf(['user', 'forum', None])]), max_entries=2)

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


class ThreadPostListForm(FlaskForm):
    thread = IntegerField(validators=[Required()])
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])
    sort = TextField(validators=[AnyOf(['flat', 'tree', 'parent_tree', None])])

    def get_post_list_data(self):
        thread = Thread.query.get_or_404(self.thread.data)
        qs = thread.posts.filter(Post.isDeleted==False)
        options = self.data

        if options.get('since'):
            try:
                date = datetime.strptime(options.get('since'), DATETIME)
                qs = qs.filter(Post.date >= date)
            except ValueError:
                raise RequestNotValid


        if self.sort.data == 'parent_tree':
            # Parent tree sorting
            def get_child_posts(post):
                pass

            qs = qs.filter(Post.parent_id==None)
        elif self.sort.data == 'tree':
            # Tree sorting
            child = aliased(Post)
            qs = qs.join(child, Post.id==child.parent_id)

            if options.get('order') == 'asc':
                qs = qs.order_by(Post.date, child.date)
            else:
                qs = qs.order_by(db.desc(Post.date), child.date)

            post_list = qs.all()

            data = {}
            # for post in post_list:
            #     if post.parent_id

        else:
            # Simple sorting
            if options.get('order') == 'asc':
                qs = qs.order_by(Post.date)
            else:
                qs = qs.order_by(db.desc(Post.date))

            if options.get('limit'):
                try:
                    qs = qs.limit(int(options.get('limit')))
                except ValueError:
                    raise IncorrectRequest

            return [p.serialize() for p in qs.all()]
