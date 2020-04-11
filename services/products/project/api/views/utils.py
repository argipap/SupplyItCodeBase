# project/api/views/utils.py


import json
from functools import wraps

import requests
from flask import request, current_app


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            "status": "error",
            "message": "Something went wrong. Please contact us.",
        }
        code = 401
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            response_object["message"] = "Provide a valid auth token."
            code = 403
            return response_object, code
        auth_token = auth_header.split(" ")[1]
        response = ensure_authenticated(auth_token)
        if not response:
            response_object["message"] = "Invalid token."
            return response_object, code
        return f(response, *args, **kwargs)

    return decorated_function


def ensure_authenticated(token):
    users_domain = current_app.config["USERS_SERVICE_URL"]
    url = f"{users_domain}/auth/status"
    bearer = f"Bearer {token}"
    headers = {"Authorization": bearer}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if (
        response.status_code == 200
        and data["status"] == "success"
        and (data["data"]["confirmed"])
    ):
        return data
    else:
        return False
