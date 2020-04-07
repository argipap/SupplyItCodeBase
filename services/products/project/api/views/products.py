# project/api/views/products.py


from flask import Blueprint
from flask_restful import Resource, Api

from project.api.models.products import ProductModel

products_blueprint = Blueprint("products", __name__, template_folder="../templates")
api = Api(products_blueprint)


class ProductsList(Resource):

    # method_decorators = {"post": [authenticate]}

    @classmethod
    def get(cls):
        response_object = {}
        products = [product.json() for product in ProductModel.query.all()]
        response_object["data"] = products
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(ProductsList, "/products")
