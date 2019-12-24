# services/users/project/api/views/test_utils.py

from functools import wraps
from flask import request, jsonify

from project.api.models.users import UserModel


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {"status": "fail", "message": "Provide a valid auth token."}
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp = UserModel.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return jsonify(response_object), 401
        user = UserModel.query.filter_by(id=resp).first()
        if not user or not user.active:
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)

    return decorated_function


def authenticate_restful(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {"status": "fail", "message": "Provide a valid auth token."}
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return response_object, 403
        auth_token = auth_header.split(" ")[1]
        resp = UserModel.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return response_object, 401
        user = UserModel.query.filter_by(id=resp).first()
        if not user or not user.active:
            return response_object, 401
        return f(resp, *args, **kwargs)

    return decorated_function


def is_admin(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return user.admin
