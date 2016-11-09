from flask import jsonify, g, request
import json
from app import app, db
from app.utils import response
from app.handlers import IncorrectRequest, RequestNotValid

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


@app.route('/db/api/user/listFollowers/')
def user_followers():
    user = User.query.filter_by(email=request.args.get('user')).first_or_404()
    qs = user.followers

    if request.args.get('since_id'):
        try:
            qs = qs.filter_by(id >= int(request.args.get('since_id')))
        except ValueError:
            raise RequestNotValid

    if request.args.get('order') in ['desc', 'asc']:
        if request.args.get('order') == 'asc':
            qs = qs.order_by(User.name)
        else:
            qs = qs.order_by(db.desc(User.name))

    if request.args.get('limit'):
        try:
            qs = qs.limit(int(request.args.get('limit')))
        except ValueError:
            raise RequestNotValid

    return response([u.serialize() for u in qs.all()])


@app.route('/db/api/user/follow/', methods=['POST'])
def user_follow():
    form = FollowForm(data=g.data)

    if form.validate():
        user = User.query.filter_by(email=form.follower.data).first_or_404()
        user_followee = User.query.filter_by(email=form.followee.data).first_or_404()
        user.following.append(user_followee)
        user.save()
        return response(user.serialize())

    raise IncorrectRequest


@app.route('/db/api/user/unfollow/', methods=['POST'])
def user_unfollow():
    form = FollowForm(data=g.data)

    if form.validate():
        user = User.query.filter_by(email=form.follower.data).first_or_404()
        user_followee = User.query.filter_by(email=form.followee.data).first_or_404()
        user.following.remove(user_followee)
        user.save()
        return response(user.serialize())

    raise IncorrectRequest
