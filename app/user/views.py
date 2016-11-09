from flask import jsonify
import json
from app import app
from app.utils import response


@app.route('/db/api/user/create/')
def user_create():
    # sreturn json.dumps({'test': 'hello'})
    return response({
        'test': [
            1, 2, 3
        ]
    })
