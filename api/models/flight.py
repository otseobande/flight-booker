import datetime
from api.app import db
from api.constants import flight_statuses

class Flight(db.Document):
    airline = db.StringField(required=True)
    departure_time = db.DateTimeField(required=True)
    estimated_arrival_time = db.DateTimeField(required=True)
    status = db.StringField(default=flight_statuses.PENDING)
    fare = db.DecimalField(min_value=0, precision=2, required=True)
    origin = db.StringField(required=True)
    destination = db.StringField(required=True)
    max_capacity = db.IntField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
