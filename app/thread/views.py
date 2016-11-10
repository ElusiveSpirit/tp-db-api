from flask import g
from app import app
from app.handlers import IncorrectRequest
from app.utils import response

from .forms import ThreadForm


@app.route('/db/api/thread/create/', methods=['POST'])
def thread_create():
    form = ThreadForm(data=g.data)
    if form.validate():
        thread = form.save()
        return response(thread.serialize())
    raise IncorrectRequest
