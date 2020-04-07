# project/tests/test_products.py

import json
import unittest
from datetime import datetime

from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProducts(BaseTestCase):
    def test_get_zero_products(self):
        with self.client:
            response = self.client.get("/products")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)

    def test_get_all_products(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get("/products")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            self.assertIn(TestUtils.product_data["name"], data["data"][0]["name"])
            self.assertIn(TestUtils.product_data["code"], data["data"][0]["code"])
            self.assertIn(
                str(TestUtils.product_data["category_id"]),
                str(data["data"][0]["category_id"])
            )
            self.assertEqual(
                datetime.utcnow().date(),
                datetime.strptime(
                    data["data"][0]["date_added"],
                    '%Y-%m-%d %H:%M:%S.%f'
                ).date()
            )
            self.assertEqual(None, data["data"][0]["date_updated"])


if __name__ == "__main__":
    unittest.main()
