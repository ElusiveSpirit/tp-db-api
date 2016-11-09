"""Imports modules and handlers"""

# errors
from app import handlers


# import all modules
import app.common
import app.user


from flask import json, request, g
from app import app
from app.handlers import RequestNotValid

@app.before_request
def serialize():
    if request.method == 'POST':
        try:
            g.data = json.loads(request.data)
        except:
            raise RequestNotValid
