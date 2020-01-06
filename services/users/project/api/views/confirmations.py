# project/api/views/confirmations.py
import os
import traceback
from time import time
from flask import Blueprint, make_response, render_template, current_app
from flask_restful import Resource, Api

from project.api.models.confirmations import ConfirmationModel
from project.api.models.users import UserModel
from project.utils.mailgun import MailGunException

confirmations_blueprint = Blueprint(
    "confirmations", __name__, url_prefix="/auth", template_folder="../templates"
)
api = Api(confirmations_blueprint)


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """Returns confirmation html page"""

        response_object = {"status": "fail", "message": "Invalid Payload"}
        confirmation = ConfirmationModel.find_by_id(_id=confirmation_id)
        if not confirmation:
            response_object["message"] = "Confirmation reference not found"
            return response_object, 404
        if confirmation.expired:
            response_object["message"] = "The link has expired"
            return response_object, 400
        if confirmation.confirmed:
            response_object["message"] = "Registration has already been confirmed"
            return response_object, 400

        confirmation.confirmed = True
        confirmation.save_to_db()
        headers = {"Content-type": "text/html"}
        return make_response(
            render_template(
                "confirmation_page.html",
                email=confirmation.user.email,
                login_uri=f"{current_app.config.get('REACT_APP_USERS_SERVICE_URL')}"
                f"/login",
            ),
            200,
            headers,
        )
        # return redirect(
        # f"{os.env("REACT_APP_USERS_SERVICE_URL")}/confirmation", code=302
        # )
        # response_object["message"] = "User activated"
        # response_object["status"] = "success"
        # return response_object, 200


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """Returns confirmation for specific user"""

        response_object = {"status": "fail"}
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return response_object, 404
        else:
            response_object["status"] = "success"
            response_object["current_time"] = int(time())
            response_object["confirmation"] = [
                each.json()
                for each in user.confirmation.order_by(ConfirmationModel.expire_at)
            ]
            return response_object, 200

    @classmethod
    def post(cls, user_id: int):
        """Resend confirmation email"""

        response_object = {"status": "fail", "message": "User Not found"}
        user = UserModel.find_by_id(_id=user_id)
        if not user:
            return response_object, 404
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    response_object["message"] = "Already confirmed"
                    return response_object, 400
                confirmation.force_to_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_mail()
            response_object["status"] = "success"
            response_object["message"] = "Email confirmation successfully resent"
            return response_object, 201
        except MailGunException as e:
            response_object["message"] = str(e)
            user.delete_from_db()
            return response_object, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            response_object[
                "message"
            ] = "Internal Server Error. Failed to resend confirmation email"
            return response_object, 500


api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
