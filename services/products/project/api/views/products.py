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


class ProductById(Resource):

    # method_decorators = {"post": [authenticate]}

    @classmethod
    def get(cls, product_id):
        response_object = {
            "status": "fail",
            "message": f"product with id: {product_id} does not exist",
        }
        try:
            product = ProductModel.find_by_id(_id=int(product_id))
            if product:
                response_object["status"] = "success"
                response_object["data"] = product.json()
                response_object.pop("message")
                return response_object, 200
            return response_object, 404
        except ValueError:
            response_object["message"] = "Product identifier (id) should be int"
            return response_object, 404
    
    
class ProductByName(Resource):

    # method_decorators = {"post": [authenticate]}

    @classmethod
    def get(cls, product_name):
        response_object = {
            "status": "fail",
            "message": f"product with name: {product_name} does not exist",
        }
        product = ProductModel.find_by_name(product_name=product_name)
        if product:
            response_object["status"] = "success"
            response_object["data"] = product.json()
            response_object.pop("message")
            return response_object, 200
        return response_object, 404


class ProductByCode(Resource):

    # method_decorators = {"post": [authenticate]}

    @classmethod
    def get(cls, product_code):
        response_object = {
            "status": "fail",
            "message": f"product with code: {product_code} does not exist",
        }
        product = ProductModel.find_by_code(product_code=product_code)
        if product:
            response_object["status"] = "success"
            response_object["data"] = product.json()
            response_object.pop("message")
            return response_object, 200
        return response_object, 404


api.add_resource(ProductsList, "/products")
api.add_resource(ProductById, "/products/id/<product_id>")
api.add_resource(ProductByName, "/products/name/<product_name>")
api.add_resource(ProductByCode, "/products/code/<product_code>")
