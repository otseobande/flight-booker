import math
from flask import request
from flask_restful import Resource

# models
from api.models.flight import Flight

# schema
from api.schema.flight import FlightSchema

# decorators
from api.decorators.catch_validation_errors import catch_validation_errors
from api.decorators.auth import login_required



class FlightList(Resource):
    flight_schema = FlightSchema()

    @login_required
    @catch_validation_errors
    def post(self):
        request_data = request.get_json(force=True)

        data = self.flight_schema.load(request_data)

        flight = Flight(**data)
        flight.save()

        return {
            'status': 'success',
            'data': {
                'flight': self.flight_schema.dump(flight)
            }
        }, 201

    @login_required
    def get(self):
        try:
            limit = int(request.args.get('limit', 10))
            page = int(request.args.get('page', 1))
        except ValueError:
            limit = 10
            page = 1

        offset = (page - 1) * limit

        flights = Flight.objects.order_by('-created_at').skip(offset).limit(limit)
        flight_count = Flight.objects.count()

        return {
            'status': 'success',
            'data': {
                'flights': self.flight_schema.dump(flights, many=True),
                'meta': {
                    'current_page': page,
                    'limit': limit,
                    'total_items': flight_count,
                    'no_of_pages': math.ceil(flight_count / limit)
                }
            }
        }
