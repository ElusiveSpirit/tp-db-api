from flask import jsonify, g, request
from app import db
from functools import wraps

# responses
def base_response(code, data=None):
    return jsonify(
        code=code,
        response=data
    )


def response(data):
    return base_response(0, data)


def form_valid(form_class, method='POST', flat=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if method == 'POST':
                form = form_class(data=g.data)
            else:
                form = form_class(data=request.args.to_dict(flat=flat))
            if form.validate():
                return f(form, *args, **kwargs)
            raise IncorrectRequest
        return wrapper
    return decorator


class Model(db.Model):
    """Common SQLAlchemy model with save and create methods"""
    __abstract__ = True

    def create(self):
        self.save()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
