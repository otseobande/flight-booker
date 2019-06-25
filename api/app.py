from flask import Flask, Blueprint, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config.from_object('api.config.Config')

@app.route('/')
def route_path():
    return jsonify({
        'message': 'Welcome to Flight booker API'
    })
