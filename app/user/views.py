from flask import jsonify, g, request
import json
from app import app, db
from app.utils import response
from app.handlers import IncorrectRequest, RequestNotValid
from app.utils import form_valid

from .models import User, special_filter
from .forms import get_user_form, FollowForm, UpdateUserForm, UserPostListForm


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
    return response(g.user.serialize())


@app.route('/db/api/user/updateProfile/', methods=['POST'])
def user_update():
    form = UpdateUserForm(data=g.data)
    if form.validate():
        user = User.query.filter_by(email=form.user.data).first_or_404()
        user.name = form.name.data
        user.about = form.about.data
        user.save()
        return response(user.serialize())

    raise IncorrectRequest


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


@app.route('/db/api/user/listPosts/')
@form_valid(UserPostListForm, 'GET', True)
def user_posts(form):
    return response(form.get_post_list_data())


@app.route('/db/api/user/listFollowers/')
def user_followers():
    qs = special_filter(g.user.followers, request.args)
    return response([u.serialize() for u in qs.all()])


@app.route('/db/api/user/listFollowing/')
def user_following():
    qs = special_filter(g.user.following, request.args)
    return response([u.serialize() for u in qs.all()])
