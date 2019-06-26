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
