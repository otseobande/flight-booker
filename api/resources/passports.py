import io
import urllib
import bson
from flask import request, g, send_file
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import NotUniqueError

# schemas
from api.schema.user import UserSchema, UserLoginSchema

# models
from api.models.user import User

# decorators
from api.decorators.auth import login_required

class Passport(Resource):
    @login_required
    def post(self):
        user = User.objects.get(id=g.user_id)
        image = request.files['image'] if request.files.get('image') else None

        if not image:
            return {
                'status': 'error',
                'errors': {
                    'image': ['Missing data for required field.']
                }
            }, 400

        if not any(extension in image.filename for extension in ['.jpg', '.png']):
            return {
                'status': 'error',
                'errors': {
                    'image': ['Only .jpg and .png file extensions are allowed.']
                }
            }, 400

        if hasattr(user, 'passport_photo'):
            user.passport_photo.delete()
            user.save()

        user.passport_photo.new_file()
        user.passport_photo.write(image)
        user.passport_photo.close()

        user.passport_photo_url = '/v1/passports/{0}/{1}'.format(
            str(user.id),
            urllib.parse.quote(image.filename)
        )
        user.save()


        return {
            'status': 'success',
            'message': 'Passport photo uploaded successfully',
            'data': {
                'user': UserSchema().dump(user)
            }
        }

class ViewPassport(Resource):
    def get(self, user_id, image_name):
        try:
            if not bson.objectid.ObjectId.is_valid(user_id):
                return '', 404

            user = User.objects.get(id=user_id)

            return send_file(
                io.BytesIO(user.passport_photo.read()),
                attachment_filename=image_name
            )

        except User.DoesNotExist:
            return '', 404
