# services/users/project/api/auth.py

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
from marshmallow import ValidationError

from project.api.models.users import UserModel
from project.api.schemas.users import UserSchema
from project import db, bcrypt
from project.api.views.errors import InternalServerError

auth_blueprint = Blueprint("auth", __name__)
user_schema = UserSchema()


@auth_blueprint.route("/auth/register", methods=["POST"])
def register_user():
    response_object = {"status": "fail", "message": "Invalid payload."}
    try:
        # get json data
        json_data = request.get_json()
        new_user = user_schema.load(json_data)
    except ValidationError as err:
        response_object["message"] = err.messages
        return response_object, 400

    try:
        # check for existing user
        user = UserModel.query.filter(
            or_(
                UserModel.username == new_user.username,
                UserModel.email == new_user.email,
            )
        ).first()
        if not user:
            # add new user to db
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object["status"] = "success"
            response_object["message"] = "Successfully registered."
            response_object["auth_token"] = auth_token.decode()
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That user already exists."
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_object), 400


@auth_blueprint.route("/auth/login", methods=["POST"])
def login_user():
    """ User login route method.
        For checking login password (bcrypt.check_password_hash function)
        against stored encrypted password in database we update password of user_data
        object to be equal with the one of request data. This is essential since with
        Marshmallow serialization, password of user_data object is being loaded from
        UserModel and thus is encrypted. """

    response_object = {"status": "fail", "message": "Invalid payload."}
    try:
        # get json data
        json_data = request.get_json()
        user_data = user_schema.load(json_data)
        user_data.password = json_data["password"]
    except ValidationError as err:
        response_object["message"] = err.messages
        return response_object, 400
    except ValueError as err:
        response_object["message"] = str(err)
        return response_object, 400

    try:
        # fetch the user data
        user = UserModel.query.filter_by(email=user_data.email).first()
        if user and bcrypt.check_password_hash(user.password, user_data.password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object["status"] = "success"
                response_object["message"] = "Successfully logged in."
                response_object["auth_token"] = auth_token.decode()
                return jsonify(response_object), 200
        else:
            response_object["message"] = "User does not exist or password is invalid."
            return jsonify(response_object), 404
    except InternalServerError:
        response_object["message"] = "Try again."
        return jsonify(response_object), 500


@auth_blueprint.route("/auth/logout", methods=["GET"])
def logout_user():
    response_object = {"status": "fail", "message": "Provide a valid auth token."}
    # get auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = UserModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response_object["status"] = "success"
            response_object["message"] = "Successfully logged out."
            return jsonify(response_object), 200
        else:
            response_object["message"] = resp
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403


@auth_blueprint.route("/auth/status", methods=["GET"])
def get_user_status():
    response_object = {"status": "fail", "message": "Provide a valid auth token."}
    # get auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = UserModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = UserModel.query.filter_by(id=resp).first()
            user_data = user_schema.dump(user)
            response_object["status"] = "success"
            response_object["message"] = "Success."
            response_object["data"] = user_data
            return jsonify(response_object), 200
        response_object["message"] = resp
        return jsonify(response_object), 401
    else:
        return jsonify(response_object), 401
