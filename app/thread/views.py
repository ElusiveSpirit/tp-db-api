from flask import g, request
from app import app
from app.handlers import IncorrectRequest
from app.utils import response, form_valid

from .forms import (ThreadForm, ThreadCloseForm, ThreadRemoveForm, ThreadDetailForm,
                    ThreadListForm, ThreadRestoreForm, ThreadOpenForm, ThreadSubscribeForm,
                    ThreadVoteForm, ThreadPostListForm, ThreadUpdateForm)


@app.route('/db/api/thread/create/', methods=['POST'])
@form_valid(ThreadForm)
def thread_create(form):
    thread = form.save()
    return response(thread.serialize())


@app.route('/db/api/thread/details/')
@form_valid(ThreadDetailForm, 'GET')
def thread_detail(form):
    return response(form.get_thread_data())


@app.route('/db/api/thread/list/')
def thread_list():
    form = ThreadListForm(data=request.args.to_dict(flat=True))
    if form.validate():
        return response(form.get_thread_list_data())
    raise IncorrectRequest


@app.route('/db/api/thread/vote/', methods=['POST'])
@form_valid(ThreadVoteForm)
def thread_vote(form):
    return response(form.update_vote())


@app.route('/db/api/thread/update/', methods=['POST'])
@form_valid(ThreadUpdateForm)
def thread_update(form):
    return response(form.update())


@app.route('/db/api/thread/open/', methods=['POST'])
@form_valid(ThreadOpenForm)
def thread_open(form):
    form.open()
    return response({'thread': form.thread.data})


@app.route('/db/api/thread/close/', methods=['POST'])
@form_valid(ThreadCloseForm)
def thread_close(form):
    form.close()
    return response({'thread': form.thread.data})


@app.route('/db/api/thread/restore/', methods=['POST'])
@form_valid(ThreadRestoreForm)
def thread_restore(form):
    form.restore()
    return response({'thread': form.thread.data})


@app.route('/db/api/thread/remove/', methods=['POST'])
@form_valid(ThreadRemoveForm)
def thread_remove(form):
    form.remove()
    return response({'thread': form.thread.data})


@app.route('/db/api/thread/subscribe/', methods=['POST'])
@form_valid(ThreadSubscribeForm)
def thread_subscribe(form):
    form.subscribe()
    return response({
        'thread': form.thread.data,
        'user': form.user.data
    })


@app.route('/db/api/thread/unsubscribe/', methods=['POST'])
@form_valid(ThreadSubscribeForm)
def thread_unsubscribe(form):
    form.unsubscribe()
    return response({
        'thread': form.thread.data,
        'user': form.user.data
    })


@app.route('/db/api/thread/listPosts/')
@form_valid(ThreadPostListForm, 'GET', True)
def thread_post_list(form):
    res = form.get_post_list_data()
    return response(res if res else [])

