from functools import wraps
from marshmallow import ValidationError

def catch_validation_errors(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValidationError as err:
            return {
                'status': 'error',
                'errors': err.messages
            }, 400

    return wrapper
