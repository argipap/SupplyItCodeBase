# services/users/project/tests/test_user_model.py


import unittest
import json

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
        self.assertTrue(user.password)

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

    def test_passwords_are_random(self):
        user_one = TestData.add_user(**TestData.user_data_1)
        user_two = TestData.add_user(**TestData.user_data_2)
        self.assertNotEqual(user_one.password, user_two.password)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    dict(username="michael", email="michael@reallynotreal.com")
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                "Missing data for required field.", data["message"]["password"]
            )
            self.assertIn("fail", data["status"])

    def test_encode_auth_token(self):
        user = TestData.add_user(**TestData.user_data_1)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = TestData.add_user(**TestData.user_data_1)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(UserModel.decode_auth_token(auth_token), user.id)


if __name__ == "__main__":
    unittest.main()
