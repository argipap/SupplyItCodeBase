import json

from project.api.models.users import UserModel
from project.tests.data import TestData
from project import db


def user_login(user_data, client):
    TestData.add_user(**user_data)
    user = UserModel.query.filter_by(email=user_data["email"]).first()
    user.admin = True
    db.session.commit()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": user_data["email"], "password": user_data["password"]}
        ),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    return token
