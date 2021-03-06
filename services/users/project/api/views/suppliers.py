# project/api/views/suppliers.py


from flask import Blueprint
from flask_restful import Resource, Api
from project.api.models.suppliers import SupplierModel

suppliers_blueprint = Blueprint(
    "suppliers", __name__, url_prefix="/users", template_folder="../templates"
)
api = Api(suppliers_blueprint)


class SuppliersList(Resource):
    @classmethod
    def get(cls):
        response_object = {}
        suppliers = [supplier.json() for supplier in SupplierModel.query.all()]
        response_object["data"] = suppliers
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(SuppliersList, "/suppliers")
