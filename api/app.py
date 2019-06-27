from flask import Flask, Blueprint, jsonify
import logging
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from flask_cors import CORS

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app = Flask(__name__)

CORS(app)

app.config.from_object('api.config.Config')
db = MongoEngine(app)

# resources
from api.resources.users import (
    UserRegister,
    UserLogin
)
from api.resources.flights import FlightList
from api.resources.flight_tickets import (
    FlightTicketList,
    FlightBooking
)
from api.resources.passports import (
    Passport,
    ViewPassport
)
from api.scheduler import scheduler

@app.route('/')
def route_path():
    return jsonify({
        'message': 'Welcome to Flight booker API'
    })

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)
api.add_resource(UserRegister, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(FlightList, '/flights')
api.add_resource(FlightTicketList, '/flights/<string:flight_id>/book')
api.add_resource(FlightBooking, '/flights/<string:flight_id>/bookings')
api.add_resource(Passport, '/user/upload-passport')
api.add_resource(ViewPassport, '/passports/<string:user_id>/<string:image_name>')

app.register_blueprint(api_blueprint, url_prefix='/v1')
