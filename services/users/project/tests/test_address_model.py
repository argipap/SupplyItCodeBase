# services/users/project/tests/test_address_model.py


import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestAddressModel(BaseTestCase):
    def test_add_address(self):
        address = TestUtils.add_address(**TestData.address_data)
        self.assertTrue(address.id)
        self.assertEqual(address.street_name, TestData.address_data["street_name"])
        self.assertEqual(address.street_number, TestData.address_data["street_number"])
        self.assertEqual(address.city, TestData.address_data["city"])
        self.assertEqual(address.zip_code, TestData.address_data["zip_code"])

    def test_deserialization(self):
        address = TestUtils.add_address(**TestData.address_data)
        self.assertTrue(isinstance(address.json(), dict))


if __name__ == "__main__":
    unittest.main()
