from flask import jsonify, g, request
import json
from app import app, db
from app.utils import response
from app.handlers import IncorrectRequest

from .models import User
from .forms import get_user_form, FollowForm


@app.route('/db/api/user/create/', methods=['POST'])
def user_create():
    form = get_user_form(g.data)

    if form.validate():
        user = User(**form.data)
        user.create()
        return response(user.serialize(less=True))

    raise IncorrectRequest


@app.route('/db/api/user/details/')
def user_detail():
    user = User.query.filter_by(email=request.args.get('user')).first_or_404()
    return response(user.serialize())


@app.route('/db/api/user/follow/', methods=['POST'])
def user_follow():
    form = FollowForm(data=g.data)

    if form.validate():
        print(form.follower.data)
        user = User.query.filter_by(email=form.follower.data).first_or_404()
        print(form.followee.data)
        user_followee = User.query.filter_by(email=form.followee.data).first_or_404()
        user.following.append(user_followee)
        user.save()
        return response(user.serialize())

    raise IncorrectRequest
