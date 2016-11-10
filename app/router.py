"""Imports modules and handlers"""

# errors
from app import handlers


# import all modules
# from config import MODULES
# map(__import__, ['app.%s' % m for m in MODULES])
import app.common
import app.forum
import app.user


from flask import json, request, g
from app import app
from app.user.models import User
from app.handlers import RequestNotValid


@app.before_request
def serialize():
    if request.method == 'POST':
        try:
            g.data = json.loads(request.data)
        except:
            raise RequestNotValid
    else:
        if 'user' in request.args:
            g.user = User.query.filter_by(
                email=request.args.get('user')).first_or_404()
