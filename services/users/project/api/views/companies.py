# project/api/views/companies.py


from flask import Blueprint
from flask_restful import Resource, Api

from project.api.models.companies import CompanyModel
from project.api.views.utils import authenticate_restful

companies_blueprint = Blueprint("companies", __name__, url_prefix="/users", template_folder="../templates")
api = Api(companies_blueprint)


class CompaniesList(Resource):
    method_decorators = {"post": [authenticate_restful]}

    @classmethod
    def get(cls):
        response_object = {}
        companies = [company.json() for company in CompanyModel.query.all()]
        response_object["data"] = companies
        response_object["status"] = "success"
        return response_object, 200


api.add_resource(CompaniesList, "/companies")
