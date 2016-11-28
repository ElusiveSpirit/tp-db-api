from flask import g, request
from app import app
from app.handlers import IncorrectRequest
from app.utils import response, form_valid

from .forms import (PostForm, PostVoteForm, PostCreateForm,
                    PostDetailForm, PostUpdateForm, PostListForm)


@app.route('/db/api/post/create/', methods=['POST'])
@form_valid(PostCreateForm)
def post_create(form):
    post = form.save()
    return response(post.serialize())


@app.route('/db/api/post/details/')
@form_valid(PostDetailForm, 'GET')
def post_detail(form):
    return response(form.get_post_data())


@app.route('/db/api/post/remove/', methods=['POST'])
@form_valid(PostForm)
def post_remove(form):
    form.remove()
    return response({
        'post': form.post_obj.id
    })


@app.route('/db/api/post/restore/', methods=['POST'])
@form_valid(PostForm)
def post_restore(form):
    form.restore()
    return response({
        'post': form.post_obj.id
    })


@app.route('/db/api/post/vote/', methods=['POST'])
@form_valid(PostVoteForm)
def post_vote(form):
    form.update_vote()
    return response(form.post_obj.serialize())


@app.route('/db/api/post/update/', methods=['POST'])
@form_valid(PostUpdateForm)
def post_update(form):
    form.update()
    return response(form.post_obj.serialize())


@app.route('/db/api/post/list/')
@form_valid(PostListForm, 'GET', True)
def post_list(form):
    return response(form.get_post_list_data())

