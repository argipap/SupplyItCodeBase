# project/api/views/products.py


from flask import Blueprint, request
from flask_restful import Resource, Api

from project import db
from project.api.models.product_categories import ProductCategoryModel
from project.api.models.products import ProductModel

products_blueprint = Blueprint("products", __name__, template_folder="../templates")
api = Api(products_blueprint)


class Products(Resource):

    # method_decorators = {"post": [authenticate]}

    @classmethod
    def get(cls):
        response_object = {}
        products = [product.json() for product in ProductModel.query.all()]
        response_object["data"] = products
        response_object["status"] = "success"
        return response_object, 200

    @classmethod
    def post(cls):
        response_object = {
            "status": "fail",
            "message": "Invalid Payload.",
        }
        json_data = request.get_json()
        if not json_data or not isinstance(json_data, dict):
            return response_object, 400
        try:
            code = json_data["code"]
            name = json_data["name"]
            if ProductModel.already_exists(name=name, code=code):
                response_object[
                    "message"
                ] = "Sorry. Product with same name or code already exists"
                return response_object, 400
            category = ProductCategoryModel.find_by_category(json_data["category"])
            if not category:
                response_object["message"] = "Sorry. This category does not exist"
                return response_object, 400
            category_id = category.id
            quantity = json_data["quantity"] if "quantity" in json_data else None
            image = json_data["image"] if "image" in json_data else None
            new_product = ProductModel(
                name=name,
                code=code,
                category_id=category_id,
                quantity=quantity,
                image=image,
            )
            new_product.save_to_db()
            response_object["status"] = "success"
            response_object["message"] = f"{new_product.name} was added!"
            return response_object, 201
        except KeyError as err:
            db.session.rollback()
            response_object[
                "message"
            ] = f"Invalid Payload. Mandatory field {str(err)} is missing"
            return response_object, 400


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


api.add_resource(Products, "/products")
api.add_resource(ProductById, "/products/id/<product_id>")
api.add_resource(ProductByName, "/products/name/<product_name>")
api.add_resource(ProductByCode, "/products/code/<product_code>")
