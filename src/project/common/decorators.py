from functools import wraps
from flask import make_response, request
from project.users.service import UserService

from .helpers import get_token


def require_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token(request.headers, request.args)
        if not token:
            return make_response('No token provided', 401)
        user = UserService.get_user_from_token(token)
        if not user:
            return make_response('Invalid token', 401)
        kwargs['user'] = user
        kwargs['token'] = token
        return f(*args, **kwargs)

    return decorated_function
