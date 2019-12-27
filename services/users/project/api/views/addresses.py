# project/api/views/addresses.py


from flask import Blueprint
from flask_restful import Resource, Api

from project.api.models.addresses import AddressModel

addresses_blueprint = Blueprint(
    "addresses", __name__, url_prefix="/users", template_folder="../templates"
)
api = Api(addresses_blueprint)


class AddressList(Resource):
    @classmethod
    def get(cls):
        response_object = {}
        addresses = [address.json() for address in AddressModel.query.all()]
        response_object["data"] = addresses
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(AddressList, "/addresses")
