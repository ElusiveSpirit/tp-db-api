from flask import g, request
from app import app
from app.handlers import IncorrectRequest, RequestNotValid
from app.utils import response

from .forms import ForumForm, ForumDetailForm


@app.route('/db/api/forum/create/', methods=['POST'])
def forum_create():
    form = ForumForm(data=g.data)
    if form.validate():
        forum = form.save()
        return response(forum.serialize(less=True))
    raise IncorrectRequest


@app.route('/db/api/forum/details/')
def forum_detail():
    form = ForumDetailForm(data=request.args.to_dict(flat=True))
    if form.validate():
        return response(form.get_forum_data())
    raise IncorrectRequest
