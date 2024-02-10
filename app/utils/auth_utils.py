from flask import session
from functools import wraps

from app.exceptions.custom_exceptions import UnauthorizedError


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "id" not in session:
            raise UnauthorizedError(
                "Please log in to access this resource.")
        return f(*args, **kwargs)
    return decorated_function
