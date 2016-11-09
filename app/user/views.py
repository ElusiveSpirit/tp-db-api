from flask import jsonify, g
import json
from app import app, db
from app.utils import response
from app.handlers import IncorrectRequest

from .models import User
from .forms import get_user_form


@app.route('/db/api/user/create/', methods=['POST'])
def user_create():
    form = get_user_form(g.data)

    if form.validate():
        user = User(**form.data)
        user.save()
        return response(form.data)

    raise IncorrectRequest
