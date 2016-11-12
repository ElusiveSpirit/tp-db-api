from flask import g, request
from app import app
from app.handlers import IncorrectRequest
from app.utils import response

from .forms import (ThreadForm, ThreadCloseForm, ThreadRemoveForm, ThreadDetailForm,
                    ThreadListForm)


@app.route('/db/api/thread/create/', methods=['POST'])
def thread_create():
    form = ThreadForm(data=g.data)
    if form.validate():
        thread = form.save()
        return response(thread.serialize())
    raise IncorrectRequest


@app.route('/db/api/thread/details/')
def thread_detail():
    form = ThreadDetailForm(data=request.args.to_dict(flat=False))
    if form.validate():
        return response(form.get_thread_data())
    raise IncorrectRequest


@app.route('/db/api/thread/list/')
def thread_list():
    form = ThreadListForm(data=request.args.to_dict(flat=True))
    if form.validate():
        return response(form.get_thread_list_data())
    print(form.errors)
    raise IncorrectRequest


@app.route('/db/api/thread/close/', methods=['POST'])
def thread_close():
    form = ThreadCloseForm(data=g.data)
    if form.validate():
        form.close()
        return response({'thread': form.thread.data})
    raise IncorrectRequest


@app.route('/db/api/thread/remove/', methods=['POST'])
def thread_remove():
    form = ThreadRemoveForm(data=g.data)
    if form.validate():
        form.remove()
        return response({'thread': form.thread.data})
    raise IncorrectRequest
