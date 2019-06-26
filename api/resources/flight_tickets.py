from flask import request, g
from flask_restful import Resource
import bson

# models
from api.models.flight_ticket import FlightTicket
from api.models.flight import Flight
from api.models.user import User

# schemas
from api.schema.flight_ticket import FlightTicketSchema

# decorators
from api.decorators.auth import login_required

class FlightTicketList(Resource):
    flight_ticket_schema = FlightTicketSchema()

    @login_required
    def post(self, flight_id):
        try:
            if not bson.objectid.ObjectId.is_valid(flight_id):
                return {
                    'status': 'error',
                    'message': 'Flight not found.'
                }, 404

            user = User.objects.get(id=g.user_id)
            flight = Flight.objects.get(id=flight_id)

            number_of_bookings = FlightTicket.objects(flight=flight).count()

            if number_of_bookings >= flight.max_capacity:
                return {
                    'status': 'error',
                    'message': 'Flight is full and cannot be booked'
                }, 422

            flight_ticket = FlightTicket(
                flight=flight,
                user=user
            )
            flight_ticket.save()

            return {
                'status': 'success',
                'data': {
                    'flight_ticket': self.flight_ticket_schema.dump(flight_ticket)
                }
            }, 201

        except Flight.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Flight not found.'
            }, 404
