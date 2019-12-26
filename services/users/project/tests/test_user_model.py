# services/users/project/tests/test_user_model.py


import unittest
import json

from project import db
from project.api.models.users import UserModel
from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils

from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = UserModel(**TestData.user_data_model_1)
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, TestData.user_data_model_1["username"])
        self.assertEqual(user.email, TestData.user_data_model_1["email"])
        self.assertTrue(user.active)
        self.assertTrue(user.password)
        self.assertFalse(user.admin)

    def test_add_user_duplicate_username(self):
        user_data = TestData.user_data_model_1
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        duplicate_user = UserModel(**user_data)
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user_data = TestData.user_data_model_1
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        duplicate_user = UserModel(**user_data)
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestUtils.add_user(**TestData.user_data_model_1)
        self.assertTrue(isinstance(user.json(), dict))

    def test_passwords_are_random(self):
        user_one = TestUtils.add_user(**TestData.user_data_model_1)
        user_two = TestUtils.add_user(**TestData.user_data_model_2)
        self.assertNotEqual(user_one.password, user_two.password)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        user_auth = TestData.user_data_model_1
        token = TestUtils.user_login(user_auth, self.client)
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(dict(username="test", email="test@test.com")),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_encode_auth_token(self):
        user = TestUtils.add_user(**TestData.user_data_model_1)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = TestUtils.add_user(**TestData.user_data_model_1)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(UserModel.decode_auth_token(auth_token), user.id)


if __name__ == "__main__":
    unittest.main()
