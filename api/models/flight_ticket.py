import datetime
from api.app import db
from api.constants import flight_statuses

class FlightTicket(db.Document):
    user = db.ReferenceField('User', required=True)
    flight = db.ReferenceField('Flight', required=True)
    ticket_number = db.SequenceField()
    created_at = db.DateTimeField(default=datetime.datetime.now)
