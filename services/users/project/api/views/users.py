# project/api/views/users.py


from flask import Blueprint, request, render_template
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy import exc
from project.api.models.users import UserModel
from project.api.schemas.users import UserSchema
from project import db

users_blueprint = Blueprint("users", __name__, template_folder="../templates")
api = Api(users_blueprint)
user_schema = UserSchema()


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    response_object = {}
    if request.method == "POST":
        try:
            json_data = request.get_json()
            new_user = user_schema.load(json_data)
            db.session.add(new_user)
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = f"{new_user.email} was added!"
        except ValidationError as err:
            response_object["message"] = err.messages
            return response_object, 400
    users = UserModel.query.all()
    return render_template("index.html", users=users)


class UsersPing(Resource):
    @classmethod
    def get(cls):
        return {"status": "success", "message": "pong!"}


class UsersList(Resource):
    @classmethod
    def post(cls):
        response_object = {"status": "fail", "message": "Invalid Payload"}
        try:
            json_data = request.get_json()
            new_user = user_schema.load(json_data)
        except ValidationError as err:
            response_object["message"] = err.messages
            return response_object, 400
        try:
            already_existed_user = UserModel.query.filter_by(
                email=new_user.email
            ).first()
            if not already_existed_user:
                db.session.add(new_user)
                db.session.commit()
                response_object["status"] = "success"
                response_object["message"] = f"{new_user.email} was added!"
            else:
                response_object["message"] = "Sorry. That email already exists."
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400

        return response_object, 201

    @classmethod
    def get(cls):
        response_object = {}
        users = [user_schema.dump(user) for user in UserModel.query.all()]
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
                response_object["data"] = user_schema.dump(user)
                response_object.pop("message")
                return response_object, 200
            return response_object, 404
        except ValueError:
            response_object["message"] = "Identifier (id) should be an integer"
            return response_object, 404


api.add_resource(UsersPing, "/users/ping")
api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")
