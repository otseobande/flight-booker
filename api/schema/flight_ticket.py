from marshmallow import Schema, fields
from api.schema.user import UserSchema
from api.schema.flight import FlightSchema

class FlightTicketSchema(Schema):
    id = fields.Str(dump_only=True)
    user = fields.Nested(UserSchema, exclude=['password'])
    flight = fields.Nested(FlightSchema)
    ticket_number = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
