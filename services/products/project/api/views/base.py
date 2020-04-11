# project/api/views/base.py


from flask import Blueprint, jsonify

from project.api.views.utils import authenticate


base_blueprint = Blueprint("base", __name__)


@base_blueprint.route("/products/ping", methods=["GET"])
@authenticate
def ping_pong(resp):
    return jsonify({"status": "success", "message": "pong!"})
