# services/users/project/api/auth.py
import traceback

import jwt
from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.api.models.confirmations import ConfirmationModel
from project.api.models.users import UserModel, UserType
from project import db, bcrypt
from project.api.views.errors import InternalServerError
from project.api.views.utils import (
    authenticate,
    add_wholesale_user_to_db,
    add_retail_user_to_db,
)
from project.utils.mailgun import MailGunException

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth/<user_type>/register", methods=["POST"])
def register_user(user_type):
    response_object = {"status": "fail", "message": "Invalid Payload"}
    # get json data
    json_data = request.get_json()
    if not json_data or not isinstance(json_data, dict):
        return jsonify(response_object), 400
    username = json_data.get("username")
    email = json_data.get("email")

    try:
        # check for existing user
        user = UserModel.query.filter(
            or_(UserModel.username == username, UserModel.email == email,)
        ).first()
        if not user:
            # add new user to db
            if user_type == UserType.wholesale.name:
                new_user = add_wholesale_user_to_db(**json_data)
            elif user_type == UserType.retail.name:
                new_user = add_retail_user_to_db(**json_data)
            else:
                return response_object, 400
            try:
                confirmation = ConfirmationModel(new_user.id)
                confirmation.save_to_db()
                new_user.send_confirmation_mail()
                response_object["status"] = "success"
                response_object["message"] = "Successfully registered."
                return jsonify(response_object), 201
            except MailGunException as e:
                new_user.delete_from_db()
                response_object["message"] = str(e)
                return jsonify(response_object), 500
            except Exception as e:
                traceback.print_exc()
                new_user.delete_from_db()
                response_object["message"] = str(e)
                return jsonify(response_object), 500
        else:
            response_object["message"] = "Sorry. That user already exists."
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError, TypeError):
        db.session.rollback()
        return jsonify(response_object), 400


@auth_blueprint.route("/auth/login", methods=["POST"])
def login_user():
    response_object = {"status": "fail", "message": "Invalid Payload"}
    # get json data
    json_data = request.get_json()
    if not json_data:
        return jsonify(response_object), 400
    email = json_data.get("email")
    password = json_data.get("password")
    try:
        # fetch the user data
        user = UserModel.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                auth_token = user.encode_token(user.id, "access")
                refresh_token = user.encode_token(user.id, "refresh")
                response_object["status"] = "success"
                response_object["message"] = "Successfully logged in."
                response_object["auth_token"] = auth_token.decode()
                response_object["refresh_token"] = refresh_token.decode()
                return jsonify(response_object), 200
            else:
                response_object["message"] = (
                    f"You have not confirmed registration. "
                    f"Please check your email: {user.email}"
                )
                return jsonify(response_object), 400
        else:
            response_object["message"] = "Email or password is invalid."
            return jsonify(response_object), 404
    except InternalServerError:
        response_object["message"] = "Try again."
        return jsonify(response_object), 500


@auth_blueprint.route("/auth/logout", methods=["GET"])
@authenticate
def logout_user(resp):
    response_object = {"status": "success", "message": "Successfully logged out."}
    return jsonify(response_object), 200


@auth_blueprint.route("/auth/status", methods=["GET"])
@authenticate
def get_user_status(resp):
    user = UserModel.query.filter_by(id=resp).first()
    response_object = {"status": "success", "message": "success", "data": user.json()}
    return jsonify(response_object), 200


@auth_blueprint.route("/auth/refresh", methods=["POST"])
def refresh_user_token():
    response_object = {"status": "fail", "message": "Provide a valid refresh token."}
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify(response_object), 403
    refresh_token = auth_header.split(" ")[1]

    try:
        resp = UserModel.decode_token(refresh_token)
        user = UserModel.find_by_id(resp)
        if not user:
            response_object["status"] = "fail"
            response_object["message"] = "Invalid token"
            return jsonify(response_object), 401
        new_access_token = user.encode_token(user.id, "access")
        new_refresh_token = user.encode_token(user.id, "refresh")

        response_object = {
            "status": "success",
            "access_token": new_access_token.decode(),
            "refresh_token": new_refresh_token.decode(),
        }
        return response_object, 200
    except jwt.ExpiredSignatureError:
        response_object["status"] = "fail"
        response_object["message"] = "Signature expired. Please log in again."
        return jsonify(response_object), 401
    except jwt.InvalidTokenError:
        response_object["status"] = "fail"
        response_object["message"] = "Invalid token. Please log in again.."
        return jsonify(response_object), 401
