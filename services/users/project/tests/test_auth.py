# services/users/project/tests/test_auth.py


import json
import unittest

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.data import TestData


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(TestData.user_data_1),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully registered.")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        TestData.add_user(**TestData.user_data_1)
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(TestData.user_data_1),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That user already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_duplicate_username(self):
        TestData.add_user(**TestData.user_data_1)
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(TestData.user_data_1),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That user already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                "/auth/register", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid Payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid Payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"username": "test", "password": "test"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid Payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"username": "test", "email": "test@test.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid Payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_registered_user_login(self):
        with self.client:
            user_data = TestData.user_data_1
            TestData.add_user(**user_data)
            response = self.client.post(
                "/auth/login",
                data=json.dumps(user_data),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully logged in.")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps(TestData.user_data_1),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertIn(
                "User does not exist or password is invalid.", data["message"]
            )
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        user_data = TestData.user_data_1
        TestData.add_user(**user_data)
        with self.client:
            # user login
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps(user_data),
                content_type="application/json",
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully logged out.")
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
        user_data = TestData.user_data_1
        TestData.add_user(**user_data)
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps(user_data),
                content_type="application/json",
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(
                data["message"] == "Signature expired. Please log in again."
            )
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                "/auth/logout", headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid token. Please log in again.")
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        user_data = TestData.user_data_1
        TestData.add_user(**user_data)
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps(user_data),
                content_type="application/json",
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/status", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["data"] is not None)
            self.assertTrue(data["data"]["username"] == user_data["username"])
            self.assertTrue(data["data"]["email"] == user_data["email"])
            self.assertTrue(data["data"]["active"] is True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                "/auth/status", headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid token. Please log in again.")
            self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
