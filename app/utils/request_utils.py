from json import loads, JSONDecodeError
from functools import wraps

from flask import request, g

from app.exceptions.custom_exceptions import UserActionError


def require_json_content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.content_type != "application/json":
            raise UserActionError("Invalid content type. Please send JSON.")
        try:
            g.request_json = loads(request.data)
        except JSONDecodeError as e:
            raise UserActionError("Invalid JSON: " + str(e))
        return f(*args, **kwargs)
    return decorated_function
