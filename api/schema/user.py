from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
