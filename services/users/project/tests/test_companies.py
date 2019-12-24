# project/tests/test_companies.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestCompaniesService(BaseTestCase):
    """Tests for the Companies Service."""

    def test_all_companies(self):
        """Ensure get all companies behaves correctly."""
        user_1 = TestUtils.add_user(**TestData.user_data_1)
        user_2 = TestUtils.add_user(**TestData.user_data_2)
        supplier_1 = TestUtils.add_supplier(user_1.id)
        supplier_2 = TestUtils.add_supplier(user_2.id)
        address_1 = TestUtils.add_address(**TestData.address_data)
        TestData.address_data["city"] = "Thessaloniki"
        address_2 = TestUtils.add_address(**TestData.address_data)
        company_1 = TestUtils.add_company(
            supplier_id=supplier_1.id,
            company_name="TestCompany",
            address_id=address_1.id,
        )
        company_2 = TestUtils.add_company(
            supplier_id=supplier_2.id,
            company_name="TestCompany",
            address_id=address_2.id,
        )
        with self.client:
            response = self.client.get("/users/companies")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]), 2)
            self.assertIn(company_1.company_name, str(data["data"][0]["company_name"]))
            self.assertIn(company_2.company_name, str(data["data"][1]["company_name"]))
            self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
