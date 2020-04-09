# project/tests/test_products.py

import json
import unittest

from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProducts(BaseTestCase):
    def test_get_zero_products(self):
        with self.client:
            response = self.client.get("/products")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]), 0)

    def test_get_all_products(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get("/products")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]), 1)
            self.assertEqual(product.name, data["data"][0]["name"])
            self.assertEqual(product.code, data["data"][0]["code"])
            self.assertEqual(product.category.name, data["data"][0]["category"])
            self.assertEqual(product.quantity, data["data"][0]["quantity"])

    def test_get_product_by_id(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(f"/products/id/{product.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.id, data["data"]["id"])

    def test_get_product_by_id_with_string(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get("/products/id/asfda")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn("Product identifier (id) should be int", data["message"])

    def test_get_product_by_id_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_id = 199
            response = self.client.get(f"/products/id/{dummy_id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with id: {dummy_id} does not exist", data["message"]
            )

    def test_get_product_by_name(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(f"/products/name/{product.name}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.name, data["data"]["name"])

    def test_get_product_by_name_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_name = "asdfas"
            response = self.client.get(f"/products/name/{dummy_name}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with name: {dummy_name} does not exist", data["message"]
            )

    def test_get_product_by_code(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(f"/products/code/{product.code}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.code, data["data"]["code"])

    def test_get_product_by_code_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_code = "asdfas"
            response = self.client.get(f"/products/code/{dummy_code}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with code: {dummy_code} does not exist", data["message"]
            )

    def test_add_product(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps(TestUtils.product_data),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data["status"], "success")
            self.assertEqual(
                data["message"], f"{TestUtils.product_data['name']} was added!"
            )

    def test_add_product_no_keys(self):
        with self.client:
            response = self.client.post(
                "/products", data=json.dumps({}), content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid Payload.")

    def test_add_product_missing_name_key(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps({"code": 52, "category": "meat_and_poultry"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Invalid Payload. Mandatory field 'name' is missing"
            )

    def test_add_product_missing_code_key(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps(
                    {"name": "test_product", "category": "meat_and_poultry"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Invalid Payload. Mandatory field 'code' is missing"
            )

    def test_add_product_missing_category_key(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps({"name": "test_product", "code": "52"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Invalid Payload. Mandatory field 'category' is missing",
            )

    def test_add_product_invalid_category(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps(
                    {"name": "test_product", "code": "52", "category": "test"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. This category does not exist",
            )

    def test_add_product_duplicate(self):
        with self.client:
            TestUtils.add_product(**TestUtils.product_data)
            response = self.client.post(
                "/products",
                data=json.dumps(TestUtils.product_data),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. Product with same name or code already exists"
            )

    def test_delete_product(self):
        pass

    def test_update_product(self):
        pass


if __name__ == "__main__":
    unittest.main()
