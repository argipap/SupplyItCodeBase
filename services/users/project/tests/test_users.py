# project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.data import TestData


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
        user_data = TestData.user_data_1
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps(user_data), content_type="application/json"
            )
        TestData.add_user(**user_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(f"{user_data['email']} was added!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            for key in TestData.invalid_payload_error.keys():
                self.assertIn(
                    TestData.invalid_payload_error[key], data["message"][key][0]
                )
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "test@test.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            for key in TestData.invalid_payload_error.keys():
                if key not in data["message"].keys():
                    for invalid_key in data["message"].keys():
                        self.assertIn(
                            TestData.invalid_payload_error[key],
                            data["message"][invalid_key][0],
                        )
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        user_data = TestData.user_data_1
        with self.client:
            self.client.post(
                "/users", data=json.dumps(user_data), content_type="application/json",
            )
            response = self.client.post(
                "/users", data=json.dumps(user_data), content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user_data = TestData.user_data_1
        user = TestData.add_user(**user_data)
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(user_data["username"], data["data"]["username"])
            self.assertIn(user_data["email"], data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("Identifier (id) should be an integer", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        TestData.add_user(**TestData.user_data_1)
        TestData.add_user(**TestData.user_data_2)
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(TestData.user_data_1["username"], data["data"][0]["username"])
            self.assertIn(TestData.user_data_1["email"], data["data"][0]["email"])
            self.assertIn(TestData.user_data_2["username"], data["data"][1]["username"])
            self.assertIn(TestData.user_data_2["email"], data["data"][1]["email"])
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
        TestData.add_user(**TestData.user_data_1)
        TestData.add_user(**TestData.user_data_2)
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(
                f'{TestData.user_data_1["username"]}'.encode("utf-8"), response.data
            )
            self.assertIn(
                f'{TestData.user_data_2["username"]}'.encode("utf-8"), response.data
            )

    def test_main_add_user(self):
        """
        Ensure a new user can be added to the database via a POST request.
        """
        user_data = TestData.user_data_1
        with self.client:
            response = self.client.post(
                "/",
                data=json.dumps(user_data),
                content_type="application/json",
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(f'{user_data["username"]}'.encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
