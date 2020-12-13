# services/users/project/tests/test_auth.py


import json
import unittest

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                user_data = TestData.user_wholesale_data
            else:
                user_data = TestData.user_retail_data
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps(user_data),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully registered.")
                self.assertTrue(response.content_type == "application/json")
                self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                user_data = TestData.user_wholesale_data
                TestUtils.add_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    user_type="wholesale",
                )
            else:
                user_data = TestData.user_retail_data
                TestUtils.add_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                )
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps(user_data),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Sorry. That user already exists.", data["message"])
                self.assertIn("fail", data["status"])

    def test_user_registration_duplicate_username(self):
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                user_data = TestData.user_wholesale_data
                TestUtils.add_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    user_type="wholesale",
                )
            else:
                user_data = TestData.user_retail_data
                TestUtils.add_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                )
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps(user_data),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Sorry. That user already exists.", data["message"])
                self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json(self):
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps({}),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_username(self):
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps({"email": "test@test.com", "password": "test"}),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_email(self):
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps({"username": "test", "password": "test"}),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_keys_no_password(self):
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/auth/{user_type}/register",
                    data=json.dumps({"username": "test", "email": "test@test.com"}),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_registered_user_login(self):
        for user_type in ("retail", "wholesale"):
            with self.client:
                if user_type == "retail":
                    user_data = TestData.user_retail_data
                    new_user = TestUtils.add_user(**TestData.retailer_data_model)
                else:
                    user_data = TestData.user_wholesale_data
                    new_user = TestUtils.add_user(**TestData.supplier_data_model)
                TestUtils.confirm_user(new_user.id)
                response = self.client.post(
                    "/auth/login",
                    data=json.dumps(user_data),
                    content_type="application/json",
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully logged in.")
                self.assertTrue(data["auth_token"])
                self.assertTrue(data["refresh_token"])
                self.assertTrue(response.content_type == "application/json")
                self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps(TestData.user_wholesale_data),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertIn("Email or password is invalid.", data["message"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        user_data = TestData.user_data_model_1
        user = TestUtils.add_user(**user_data)
        TestUtils.confirm_user(user.id)
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
        current_app.config["ACCESS_TOKEN_EXPIRATION"] = -1
        user_data = TestData.user_data_model_1
        new_user = TestUtils.add_user(**user_data)
        TestUtils.confirm_user(new_user.id)
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
        user_data = TestData.user_data_model_1
        user = TestUtils.add_user(**user_data)
        TestUtils.confirm_user(user.id)
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
            self.assertTrue(data["data"]["confirmed"] is True)
            self.assertFalse(data["data"]["admin"])
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
