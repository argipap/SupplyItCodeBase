# project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils
from project.api.models.users import UserModel
from project import db


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        user_auth = TestData.user_data_model_1
        token = TestUtils.user_login(user_auth, self.client)
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                new_user = TestData.user_wholesale_data
            else:
                new_user = TestData.user_retail_data
            with self.client:
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(new_user),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(f"{new_user['email']} was added!", data["message"])
                self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        user_auth = TestData.user_data_model_1
        token = TestUtils.user_login(user_auth, self.client)
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps({}),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        user_auth = TestData.user_data_model_1
        token = TestUtils.user_login(user_auth, self.client)
        for user_type in ("retail", "wholesale"):
            with self.client:
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps({"email": "test@test.com"}),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid Payload", data["message"])
                self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        user_auth = TestData.user_data_model_1
        token = TestUtils.user_login(user_auth, self.client)
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                new_user = TestData.user_wholesale_data
            else:
                new_user = TestData.user_retail_data
            with self.client:
                self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(new_user),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(new_user),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 400)
                self.assertIn("Sorry. That email already exists.", data["message"])
                self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user_data = TestData.user_data_model_1
        user = TestUtils.add_user(**user_data)
        with self.client:
            response = self.client.get(f"/users/user/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(user_data["username"], data["data"]["username"])
            self.assertIn(user_data["email"], data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get("/users/user/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("Identifier (id) should be an integer", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get("/users/user/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        TestUtils.add_user(**TestData.user_data_model_1)
        TestUtils.add_user(**TestData.user_data_model_2)
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(
                TestData.user_data_model_1["username"], data["data"][0]["username"]
            )
            self.assertIn(TestData.user_data_model_1["email"], data["data"][0]["email"])
            self.assertIn(
                TestData.user_data_model_2["username"], data["data"][1]["username"]
            )
            self.assertIn(TestData.user_data_model_2["email"], data["data"][1]["email"])
            self.assertFalse(data["data"][1]["active"])
            self.assertFalse(data["data"][1]["admin"])
            self.assertIn("success", data["status"])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        TestUtils.add_user(**TestData.user_data_model_1)
        TestUtils.add_user(**TestData.user_data_model_2)
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(
                f'{TestData.user_data_model_1["username"]}'.encode("utf-8"),
                response.data,
            )
            self.assertIn(
                f'{TestData.user_data_model_2["username"]}'.encode("utf-8"),
                response.data,
            )

    def test_main_add_user(self):
        """
        Ensure a new user can be added to the database via a POST request.
        """
        user_data = TestData.user_wholesale_data
        with self.client:
            response = self.client.post(
                "/", data=dict(**user_data), follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(f'{user_data["username"]}'.encode("utf-8"), response.data)

    def test_add_user_inactive(self):
        user_data = TestData.user_data_model_1
        TestUtils.add_user(**user_data)
        # update user
        user = UserModel.query.filter_by(email=user_data["email"]).first()
        user.active = False
        db.session.commit()
        for user_type in ("retail", "wholesale"):
            with self.client:
                resp_login = self.client.post(
                    "/auth/login",
                    data=json.dumps(
                        {"email": user_data["email"], "password": user_data["password"]}
                    ),
                    content_type="application/json",
                )
                token = json.loads(resp_login.data.decode())["auth_token"]
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(user_data),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data["status"] == "fail")
                self.assertTrue(
                    data["message"]
                    == "You have not confirmed registration. Please check your email."
                )
                self.assertEqual(response.status_code, 401)

    def test_add_user_not_admin(self):
        user_auth = TestData.user_data_model_1
        user = TestUtils.add_user(**user_auth)
        user.active = True
        db.session.add(user)
        db.session.commit()
        for user_type in ("retail", "wholesale"):
            if user_type == "wholesale":
                new_user = TestData.user_wholesale_data
            else:
                new_user = TestData.user_retail_data
            with self.client:
                resp_login = self.client.post(
                    "/auth/login",
                    data=json.dumps(
                        {"email": user_auth["email"], "password": user_auth["password"]}
                    ),
                    content_type="application/json",
                )
                token = json.loads(resp_login.data.decode())["auth_token"]
                response = self.client.post(
                    f"/users/{user_type}",
                    data=json.dumps(new_user),
                    content_type="application/json",
                    headers={"Authorization": f"Bearer {token}"},
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data["status"] == "fail")
                self.assertTrue(
                    data["message"] == "You do not have permission to do that."
                )
                self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
