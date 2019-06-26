import datetime
import bcrypt
from decouple import config as env_config
from mongoengine import signals
import jwt

from api.app import db

secret = env_config('SECRET_KEY')

class User(db.Document):
    full_name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    phone_number = db.StringField(required=True)
    address = db.StringField(required=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        changed_fields = document._get_changed_fields()

        if 'password' in changed_fields or not changed_fields:
            hashed_password = bcrypt.hashpw(document.password.encode('utf-8'), bcrypt.gensalt())

            document.password = hashed_password.decode('utf-8')

        document.updated_at = datetime.datetime.utcnow()

    def generate_token(self):
        token = jwt.encode(
            { 'id': str(self.id) },
            secret,
            algorithm='HS256'
        )

        return token.decode('utf-8')

signals.pre_save.connect(User.pre_save, sender=User)
