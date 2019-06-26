import math
from flask import request, g
from flask_restful import Resource
import bson
import datetime

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

class FlightBooking(Resource):
    flight_ticket_schema = FlightTicketSchema()

    @login_required
    def get(self, flight_id):
        try:
            if not bson.objectid.ObjectId.is_valid(flight_id):
                return {
                    'status': 'error',
                    'message': 'Flight not found.'
                }, 404

            flight = Flight.objects.get(id=flight_id)

            try:
                limit = int(request.args.get('limit', 10))
                page = int(request.args.get('page', 1))
            except ValueError:
                limit = 10
                page = 1

            offset = (page - 1) * limit

            date = request.args.get('date', None)

            if date:
                try:
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    return {
                        'status': 'error',
                        'message': 'Date should be in YYYY-MM-DD format'
                    }, 400
            else:
                date = datetime.datetime.today()

            beginning_of_day = date.replace(hour=0)
            end_of_day = date.replace(hour=23)

            flight_tickets_query = FlightTicket.objects(
                flight=flight,
                created_at__gte=beginning_of_day,
                created_at__lte=end_of_day
            )

            flight_tickets = flight_tickets_query.order_by('-created_at').skip(offset).limit(limit)
            flight_ticket_count = flight_tickets_query.count()

            return {
                'status': 'success',
                'data': {
                    'flight_tickets': self.flight_ticket_schema.dump(flight_tickets, many=True),
                    'meta': {
                        'current_page': page,
                        'limit': limit,
                        'total_items': flight_ticket_count,
                        'no_of_pages': math.ceil(flight_ticket_count / limit)
                    }
                }
            }

        except Flight.DoesNotExist:
            return {
                'status': 'error',
                'message': 'Flight not found.'
            }, 404
