# project/api/views/retailers.py


from flask import Blueprint
from flask_restful import Resource, Api
from project.api.models.retailers import RetailerModel

retailers_blueprint = Blueprint(
    "retailers", __name__, url_prefix="/users", template_folder="../templates"
)
api = Api(retailers_blueprint)


class RetailersList(Resource):
    @classmethod
    def get(cls):
        response_object = {}
        retailers = [retailer.json() for retailer in RetailerModel.query.all()]
        response_object["data"] = retailers
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(RetailersList, "/retailers")
