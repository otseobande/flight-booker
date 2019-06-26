from flask import Flask, Blueprint, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config.from_object('api.config.Config')
db = MongoEngine(app)

from api.resources.users import UserRegister

@app.route('/')
def route_path():
    return jsonify({
        'message': 'Welcome to Flight booker API'
    })

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)
api.add_resource(UserRegister, '/auth/register')

app.register_blueprint(api_blueprint, url_prefix='/v1')
