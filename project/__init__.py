# users/project/__init__.py

import os
from flask import Flask, jsonify
from flask_restful import Resource, Api


# instantiate the app
app = Flask(__name__)

api = Api(app)

# import app settings and config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


class UsersPing(Resource):
    @classmethod
    def get(cls):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(UsersPing, '/users/ping')
