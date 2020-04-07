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
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get("/products")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            self.assertEqual(product.name, data["data"][0]["name"])
            self.assertEqual(product.code, data["data"][0]["code"])
            self.assertEqual(product.category_id, data["data"][0]["category_id"])
            self.assertEqual(product.quantity, data["data"][0]["quantity"])


if __name__ == "__main__":
    unittest.main()
