# services/users/project/tests/test_user_model.py


import unittest

from project import db
from project.api.models.users import UserModel
from project.tests.base import BaseTestCase
from project.tests.data import TestData
from project.api.schemas.users import UserSchema

from sqlalchemy.exc import IntegrityError

user_schema = UserSchema()


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = UserModel(**TestData.user_data_model)
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, TestData.user_data_model["username"])
        self.assertEqual(user.email, TestData.user_data_model["email"])
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user_data = TestData.user_data_model
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        duplicate_user = UserModel(**user_data)
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user_data = TestData.user_data_model
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        duplicate_user = UserModel(**user_data)
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestData.add_user(**TestData.user_data_1)
        self.assertTrue(isinstance(user_schema.dump(user), dict))


if __name__ == "__main__":
    unittest.main()
