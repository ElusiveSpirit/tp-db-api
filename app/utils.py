from flask import jsonify
from app import db

# responses
def base_response(code, data=None):
    return jsonify(
        code=code,
        response=data
    )


def response(data):
    return base_response(0, data)


class Model(db.Model):
    __abstract__ = True

    def create(self):
        self.save()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
