# project/tests/test_stores.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestStoresService(BaseTestCase):
    """Tests for the Stores Service."""

    def test_all_companies(self):
        """Ensure get all stores behaves correctly."""
        user_1 = TestUtils.add_user(**TestData.user_data_1)
        user_2 = TestUtils.add_user(**TestData.user_data_2)
        retailer_1 = TestUtils.add_retailer(user_1.id)
        retailer_2 = TestUtils.add_retailer(user_2.id)
        address_1 = TestUtils.add_address(**TestData.address_data)
        TestData.address_data["city"] = "Thessaloniki"
        address_2 = TestUtils.add_address(**TestData.address_data)
        store_1 = TestUtils.add_store(
            retailer_id=retailer_1.id, store_name="TestStore1", address_id=address_1.id
        )
        store_2 = TestUtils.add_store(
            retailer_id=retailer_2.id, store_name="TestStore2", address_id=address_2.id
        )
        with self.client:
            response = self.client.get("/users/stores")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(store_1.store_name, str(data["data"][0]["store_name"]))
            self.assertIn(store_2.store_name, str(data["data"][1]["store_name"]))
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
