from app import app
from app.utils import base_response


class NotFound(Exception):
    status_code = 1
    msg = 'Not found'


class RequestNotValid(Exception):
    """невалидный запрос (например, не парсится json)"""
    status_code = 2
    msg = 'Request not valid'


class IncorrectRequest(Exception):
    """некорректный запрос (семантически)"""
    status_code = 3
    msg = 'Incorrect request'


class UnexpectedError(Exception):
    status_code = 4
    msg = 'Unexpected error'


class UserExists(Exception):
    status_code = 5
    msg = 'User already exists'


@app.errorhandler(NotFound)
@app.errorhandler(RequestNotValid)
@app.errorhandler(IncorrectRequest)
@app.errorhandler(UnexpectedError)
@app.errorhandler(UserExists)
def common_error_handler(error):
    return base_response(error.status_code)


@app.errorhandler(404)
def page_not_found(error):
    return base_response(1, 'Not found')

@app.errorhandler(500)
def unexpected_error(error):
    return base_response(4, 'Unexpected error')
