# project/tests/test_addresses.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestAddressesService(BaseTestCase):
    """Tests for the Addresses Service."""

    def test_all_addresses(self):
        """Ensure get all addresses behaves correctly."""
        address_1 = TestUtils.add_address(**TestData.address_data)
        address_2 = TestUtils.add_address(**TestData.address_data)
        with self.client:
            response = self.client.get("/users/addresses")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(str(address_1.json()), str(data["data"][0]))
            self.assertIn(str(address_2.json()), str(data["data"][1]))
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
