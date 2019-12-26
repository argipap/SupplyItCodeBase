# project/api/views/users.py


from flask import Blueprint, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import exc
from project.api.models.users import UserModel, UserType
from project.api.models.suppliers import SupplierModel
from project.api.models.retailers import RetailerModel
from project import db
from project.api.views.utils import (
    authenticate_restful,
    is_admin,
    add_wholesale_user_to_db,
    add_retail_user_to_db,
)

users_blueprint = Blueprint("users", __name__, template_folder="../templates")
api = Api(users_blueprint)


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        db.session.add(UserModel(username=username, email=email, password=password))
        db.session.commit()
    users = UserModel.query.all()
    return render_template("index.html", users=users)


class UsersPing(Resource):
    @classmethod
    def get(cls):
        return {"status": "success", "message": "pong!"}


class UsersListByType(Resource):

    method_decorators = {"post": [authenticate_restful]}

    @classmethod
    def post(cls, resp, user_type):
        response_object = {"status": "fail", "message": "Invalid Payload"}
        json_data = request.get_json()
        if not is_admin(resp):
            response_object["message"] = "You do not have permission to do that."
            return response_object, 401
        if not json_data or not isinstance(json_data, dict):
            return response_object, 400
        email = json_data.get("email")
        try:
            already_existed_user = UserModel.query.filter_by(email=email).first()
            if not already_existed_user:
                if user_type == UserType.wholesale.name:
                    new_user = add_wholesale_user_to_db(**json_data)
                elif user_type == UserType.retail.name:
                    new_user = add_retail_user_to_db(**json_data)
                else:
                    return response_object, 400
                response_object["status"] = "success"
                response_object["message"] = f"{new_user.email} was added!"
                return response_object, 201
            else:
                response_object["message"] = "Sorry. That email already exists."
                return response_object, 400
        except (exc.IntegrityError, ValueError, TypeError):
            db.session.rollback()
            return response_object, 400

    @classmethod
    def get(cls, user_type):
        response_object = {}
        users = [
            user.json() for user in UserModel.query.filter_by(user_type=user_type).all()
        ]
        response_object["data"] = users
        response_object["status"] = "success"
        return response_object, 200


class UsersList(Resource):
    @classmethod
    def get(cls):
        response_object = {}
        users = [user.json() for user in UserModel.query.all()]
        response_object["data"] = users
        response_object["status"] = "success"
        return response_object, 200


class Users(Resource):
    @classmethod
    def get(cls, user_id):
        """Get single user details"""
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = UserModel.query.filter_by(id=int(user_id)).first()
            if user:
                response_object["status"] = "success"
                response_object["data"] = user.json()
                response_object.pop("message")
                return response_object, 200
            return response_object, 404
        except ValueError:
            response_object["message"] = "Identifier (id) should be an integer"
            return response_object, 404


api.add_resource(UsersPing, "/users/ping")
api.add_resource(UsersListByType, "/users/<user_type>")
api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/user/<user_id>")
