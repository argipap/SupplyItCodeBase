from project.api.models.users import UserModel
from project import db


class TestData:
    user_data_1 = {
        "username": "test1",
        "email": "test1@test.com",
        "password": "123abc!",
    }
    user_data_2 = {
        "username": "test2",
        "email": "test2@test.com",
        "password": "123abc!",
    }

    user_data_model = {
        "username": "testmodel",
        "email": "testmodel@test.com",
        "password": "123abc!",
    }

    @classmethod
    def add_user(cls, username, email, password):
        user = UserModel(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user
