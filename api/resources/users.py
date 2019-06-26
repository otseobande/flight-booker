from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import NotUniqueError

from api.schema.user import UserSchema, UserLoginSchema
from api.models.user import User

# decorators
from api.decorators.catch_validation_errors import catch_validation_errors


class UserRegister(Resource):
    @catch_validation_errors
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
            }, 201

        except NotUniqueError:
            return {
                'status': 'error',
                'message': 'Email is already registered.'
            }, 409

class UserLogin(Resource):
    @catch_validation_errors
    def post(self):
        try:
            request_data = request.get_json(force=True)

            data = UserLoginSchema().load(request_data)
            user = User.objects.get(email=data['email'])

            if not user.verify_password(data['password']):
                return {
                    'status': 'error',
                    'message': 'Email or password is incorrect, please check your credentials.'
                }, 401

            return {
                'status': 'success',
                'data': {
                    'user': UserSchema(exclude=['password']).dump(user),
                    'token': user.generate_token()
                }
            }

        except User.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Email or password is incorrect, please check your credentials.'
            }, 401

