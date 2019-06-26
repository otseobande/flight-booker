from marshmallow import Schema, fields

class FlightSchema(Schema):
    id = fields.Str(dump_only=True)
    airline = fields.Str(required=True)
    departure_time = fields.DateTime(required=True)
    estimated_arrival_time = fields.DateTime(required=True)
    status = fields.Str()
    fare = fields.Float(required=True)
    origin = fields.Str(required=True)
    destination = fields.Str(required=True)
    max_capacity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
