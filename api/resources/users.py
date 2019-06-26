from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import NotUniqueError

from api.schema.user import UserSchema
from api.models.user import User


class UserRegister(Resource):
    def post(self):
        try:
            request_data = request.get_json(force=True)

            data = UserSchema().load(request_data)

            user = User(**data)
            user.save()

            token = user.generate_token()

            return {
                'status': 'success',
                'data': {
                    'user': UserSchema(exclude=['password']).dump(user),
                    'token': token
                }
            }

        except ValidationError as err:
            return {
                'status': 'error',
                'errors': err.messages
            }, 400

        except NotUniqueError:
            return {
                'status': 'error',
                'message': 'Email is already registered.'
            }, 409
