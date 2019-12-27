# project/api/views/stores.py


from flask import Blueprint
from flask_restful import Resource, Api

from project.api.models.stores import StoreModel
from project.api.views.utils import authenticate_restful

stores_blueprint = Blueprint(
    "stores", __name__, url_prefix="/users", template_folder="../templates"
)
api = Api(stores_blueprint)


class StoresList(Resource):
    method_decorators = {"post": [authenticate_restful]}

    @classmethod
    def get(cls):
        response_object = {}
        stores = [store.json() for store in StoreModel.query.all()]
        response_object["data"] = stores
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(StoresList, "/stores")
