from flask import g, request
from app import app
from app.handlers import IncorrectRequest, RequestNotValid
from app.utils import response, form_valid

from .forms import (ForumForm, ForumDetailForm, ForumUserListForm, ForumThreadListForm,
                    ForumPostListForm)


@app.route('/db/api/forum/create/', methods=['POST'])
def forum_create():
    form = ForumForm(data=g.data)
    if form.validate():
        forum = form.save()
        return response(forum.serialize())
    raise IncorrectRequest


@app.route('/db/api/forum/details/')
def forum_detail():
    form = ForumDetailForm(data=request.args.to_dict(flat=True))
    if form.validate():
        return response(form.get_forum_data())
    raise IncorrectRequest


@app.route('/db/api/forum/listUsers')
@form_valid(ForumUserListForm, 'GET')
def forum_users(form):
    return response(form.get_user_list_data())


@app.route('/db/api/forum/listThreads')
@form_valid(ForumThreadListForm, 'GET')
def forum_threads(form):
    return response(form.get_thread_list_data())


@app.route('/db/api/forum/listThreads')
@form_valid(ForumPostListForm, 'GET')
def forum_posts(form):
    return response(form.get_post_list_data())
