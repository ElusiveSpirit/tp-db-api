from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, IntegerField, FieldList, ValidationError
from wtforms.validators import Required, AnyOf
from app.handlers import IncorrectRequest

from .models import Post
from app.thread.models import Thread, magic_filter
from app.forum.models import Forum
from app.user.models import User


class PostCreateForm(FlaskForm):
    message = TextField(validators=[Required()])
    date = TextField(validators=[Required()])
    thread = IntegerField(validators=[Required()])
    user = TextField(validators=[Required()])
    forum = TextField(validators=[Required()])
    parent = TextField()
    isApproved = BooleanField(false_values=[False])
    isHighlighted = BooleanField(false_values=[False])
    isEdited = BooleanField(false_values=[False])
    isSpam = BooleanField(false_values=[False])
    isDeleted = BooleanField(false_values=[False])

    def save(self):
        parent_id = Post.query.get_or_404(int(self.parent.data)).id if self.parent.data else None
        user_id = User.query.filter_by(email=self.user.data).first_or_404().id
        forum_id = Forum.query.filter_by(short_name=self.forum.data).first_or_404().id
        thread_id = Thread.query.get_or_404(self.thread.data).id

        post = Post(
            message=self.message.data,
            user_id=user_id,
            forum_id=forum_id,
            thread_id=thread_id,
            parent_id=parent_id,
            date=self.date.data,
            isApproved=self.isApproved.data,
            isHighlighted=self.isHighlighted.data,
            isEdited=self.isEdited.data,
            isSpam=self.isSpam.data,
            isDeleted=self.isDeleted.data
        )
        post.save();
        return post


class PostForm(FlaskForm):
    post = IntegerField(validators=[Required()])

    def validate(self):
        print('validation')
        if (super(PostForm, self).validate()):
            self.post_obj = Post.query.get_or_404(self.post.data)
            return True
        return False

    def remove(self):
        self.post_obj.isDeleted = True
        self.post_obj.save()

    def restore(self):
        self.post_obj.isDeleted = False
        self.post_obj.save()


class PostUpdateForm(PostForm):
    message = TextField(validators=[Required()])

    def update(self):
        self.post_obj.message = self.message.data
        self.post_obj.save()


class PostVoteForm(PostForm):
    vote = IntegerField(validators=[AnyOf([1, -1])])

    def update_vote(self):
        if self.vote.data == 1:
            self.post_obj.likes += 1
        else:
            self.post_obj.dislikes += 1
        self.post_obj.save()


class PostDetailForm(PostForm):
    related = FieldList(TextField(), max_entries=3)

    def get_post_data(self):
        return self.post_obj.serialize(self.related.data)


class PostListForm(FlaskForm):
    thread = IntegerField()
    forum = TextField()
    since = TextField()
    limit = IntegerField()
    order = TextField(validators=[AnyOf(['asc', 'desc', None])])

    def validate_thread(self, field):
        # if both with data or not
        if (field.data and self.forum.data) or (not field.data and not self.forum.data):
            raise ValidationError

    def get_post_list_data(self):
        if self.thread.data:
            thread = Thread.query.get_or_404(self.thread.data)
            post_list_qs = thread.posts.filter(Post.isDeleted==False)
        else:
            forum = Forum.query.filter_by(short_name=self.forum.data).first_or_404()
            post_list_qs = forum.posts.filter(Post.isDeleted==False)

        return [t.serialize() for t in (magic_filter(post_list_qs, self.data, Post)).all()]

