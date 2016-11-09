from flask import jsonify

# responses
def base_response(code, data=None):
    return jsonify(
        code=code,
        response=data
    )


def response(data):
    return base_response(0, data)
