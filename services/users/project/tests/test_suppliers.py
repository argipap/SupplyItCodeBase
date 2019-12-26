# project/tests/test_suppliers.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestSuppliersService(BaseTestCase):
    """Tests for the Suppliers Service."""

    def test_all_suppliers(self):
        """Ensure get all suppliers behaves correctly."""
        user_1 = TestUtils.add_user(**TestData.user_data_model_1)
        user_2 = TestUtils.add_user(**TestData.user_data_model_2)
        TestUtils.add_supplier(user_1.id)
        TestUtils.add_supplier(user_2.id)
        with self.client:
            response = self.client.get("/users/suppliers")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(str(user_1.id), str(data["data"][0]["user_id"]))
            self.assertIn(str(user_2.id), str(data["data"][1]["user_id"]))
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
