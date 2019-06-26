from functools import wraps
import jwt
from flask import abort, request, g

from api.models.user import User


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {
                'status': 'error',
                'message': 'Token not provided or is invalid.'
            }, 401

        user_id = None
        auth_header = request.headers.get('Authorization')
        if auth_header and len(auth_header.split(" ")) == 2:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        try:
            user_id = User.decode_token(auth_token).get('id')

            g.user_id = user_id
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return {
                'status': 'error',
                'message': 'Token not provided or is invalid.'
            }, 401


        return fn(*args, **kwargs)

    return wrapper
