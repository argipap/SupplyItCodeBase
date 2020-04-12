# project/tests/test_products.py

import json
import unittest

from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProducts(BaseTestCase):
    def test_get_zero_products(self):
        with self.client:
            response = self.client.get(
                "/products", headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}")
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]), 0)

    def test_get_zero_products_by_company(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                "/products?company=test",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]), 0)

    def test_get_all_products(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                "/products", headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}")
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]), 1)
            self.assertEqual(product.name, data["data"][0]["name"])
            self.assertEqual(product.code, data["data"][0]["code"])
            self.assertEqual(product.category.name, data["data"][0]["category"])
            self.assertEqual(product.quantity, data["data"][0]["quantity"])

    def test_get_products_by_company(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                f"/products?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
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
            response = self.client.get(
                f"/products/id/{product.id}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.id, data["data"]["id"])

    def test_get_product_by_id_with_string(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                "/products/id/asfda",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn("Product identifier (id) should be int", data["message"])

    def test_get_product_by_id_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_id = 199
            response = self.client.get(
                f"/products/id/{dummy_id}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with id: {dummy_id} does not exist", data["message"]
            )

    def test_get_all_products_by_name(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                f"/products/name/{product.name}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.name, data["data"][0]["name"])

    def test_get_all_products_by_name_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_name = "asdfas"
            response = self.client.get(
                f"/products/name/{dummy_name}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with name: {dummy_name} does not exist", data["message"]
            )

    def test_get_product_by_name(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                f"/products/name/{product.name}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.name, data["data"]["name"])

    def test_get_product_by_name_not_exists(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_name = "asdfas"
            response = self.client.get(
                f"/products/name/{dummy_name}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with name: {dummy_name} does not exist", data["message"]
            )

    def test_get_product_by_name_not_exists_in_company(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        dummy_company = "asfadfa"
        with self.client:
            response = self.client.get(
                f"/products/name/{product.name}?company={dummy_company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with name: {product.name} "
                f"does not exist in company {dummy_company}",
                data["message"],
            )

    def test_get_product_by_code(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                f"/products/code/{product.code}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.code, data["data"]["code"])

    def test_get_all_products_by_code(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.get(
                f"/products/code/{product.code}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(product.code, data["data"][0]["code"])

    def test_get_product_by_code_not_exists(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_code = "asdfas"
            response = self.client.get(
                f"/products/code/{dummy_code}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with code: {dummy_code} does not exist", data["message"]
            )

    def test_get_all_products_by_code_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            dummy_code = "asdfas"
            response = self.client.get(
                f"/products/code/{dummy_code}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with code: {dummy_code} does not exist", data["message"]
            )

    def test_get_product_by_code_not_exists_in_company(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        dummy_company = "asfadfa"
        with self.client:
            response = self.client.get(
                f"/products/code/{product.code}?company={dummy_company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertIn(
                f"product with code: {product.code} "
                f"does not exist in company {dummy_company}",
                data["message"],
            )

    def test_add_product(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps(TestUtils.product_data),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data["status"], "success")
            self.assertEqual(
                data["message"],
                f"Product {TestUtils.product_data['name']} added successfully",
            )

    def test_add_product_no_keys(self):
        with self.client:
            response = self.client.post(
                "/products",
                data=json.dumps({}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
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
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
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
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
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
                data=json.dumps(
                    {"name": "test_product", "code": "52", "company": "company_1"}
                ),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
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
                    {
                        "name": "test_product",
                        "code": "52",
                        "category": "test",
                        "company": "company_1",
                    }
                ),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
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
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. Product with same name or code already exists"
            )

    def test_delete_product_by_id(self):
        # first adding a product in order to delete it
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.delete(
                f"/products/id/{product.id}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product deleted successfully")

    def test_delete_product_by_id_not_exists(self):
        with self.client:
            response = self.client.delete(
                "/products/id/199",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            self.assertFalse(response.data)
            self.assertEqual(response.status_code, 204)

    def test_delete_product_by_name(self):
        # first adding a product in order to delete it
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.delete(
                f"/products/name/{product.name}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product deleted successfully")

    def test_delete_product_by_name_not_exists(self):
        with self.client:
            response = self.client.delete(
                f"/products/name/testproduct?company=test",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            self.assertFalse(response.data)
            self.assertEqual(response.status_code, 204)

    def test_delete_product_name_company_missing(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.delete(
                f"/products/name/{product.name}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "company field is mandatory")

    def test_delete_product_by_code(self):
        # first adding a product in order to delete it
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.delete(
                f"/products/code/{product.code}?company={product.company}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product deleted successfully")

    def test_delete_product_by_code_not_exists(self):
        with self.client:
            response = self.client.delete(
                "/products/code/199.33?company=test",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            self.assertFalse(response.data)
            self.assertEqual(response.status_code, 204)

    def test_delete_product_code_company_missing(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.delete(
                f"/products/code/{product.name}",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "company field is mandatory")

    def test_update_product_by_id(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/id/{product.id}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product updated successfully")

    def test_update_product_by_id_no_data(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/id/{product.id}",
                data=json.dumps({}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid Payload.")

    def test_update_product_by_id_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        product_id = "199"
        with self.client:
            response = self.client.put(
                f"/products/id/{product_id}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], f"Product with id: {product_id} does not exist"
            )

    def test_update_product_by_id_invalid_json_keys(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/id/{product.id}",
                data=json.dumps(TestUtils.product_data_update_invalid_keys),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertIn("is not a valid request parameter", data["message"])

    def test_update_product_by_id_invalid_category(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/id/{product.id}",
                data=json.dumps(TestUtils.product_data_invalid_category),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. This product category does not exist"
            )

    def test_update_product_by_id_duplicate_code(self):
        product_1 = TestUtils.add_product(**TestUtils.product_data)
        product_2 = TestUtils.add_product(**TestUtils.product_data_update)
        with self.client:
            response = self.client.put(
                f"/products/id/{product_2.id}",
                data=json.dumps({"code": product_1.code}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertRegex(data["message"], "^Product with Key.*already exists.")

    def test_update_product_by_name(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/name/{product.name}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product updated successfully")

    def test_update_product_by_name_no_data(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/name/{product.id}",
                data=json.dumps({}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid Payload.")

    def test_update_product_by_name_invalid_json_keys(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/name/{product.name}",
                data=json.dumps(TestUtils.product_data_update_invalid_keys),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertIn("is not a valid request parameter", data["message"])

    def test_update_product_by_name_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        product_name = "anotherProduct"
        with self.client:
            response = self.client.put(
                f"/products/name/{product_name}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], f"Product with name: {product_name} does not exist"
            )

    def test_update_product_by_name_invalid_category(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/name/{product.name}",
                data=json.dumps(TestUtils.product_data_invalid_category),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. This product category does not exist"
            )

    def test_update_product_by_name_company_missing(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        new_data = dict(**TestUtils.product_data)
        new_data.pop("company")
        with self.client:
            response = self.client.put(
                f"/products/name/{product.name}",
                data=json.dumps(new_data),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                f"Invalid Payload. Mandatory field 'company' is missing",
            )

    def test_update_product_by_name_duplicate_code(self):
        product_1 = TestUtils.add_product(**TestUtils.product_data)
        product_2 = TestUtils.add_product(**TestUtils.product_data_update)
        with self.client:
            response = self.client.put(
                f"/products/name/{product_2.name}",
                data=json.dumps({"code": product_1.code, "company": product_1.company}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertRegex(data["message"], "^Product with Key.*already exists.")

    def test_update_product_by_code(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/code/{product.code}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Product updated successfully")

    def test_update_product_by_code_no_data(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/code/{product.id}",
                data=json.dumps({}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid Payload.")

    def test_update_product_by_code_invalid_json_keys(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/code/{product.code}",
                data=json.dumps(TestUtils.product_data_update_invalid_keys),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertIn("is not a valid request parameter", data["message"])

    def test_update_product_by_code_not_exists(self):
        TestUtils.add_product(**TestUtils.product_data)
        product_code = "anotherCode"
        with self.client:
            response = self.client.put(
                f"/products/code/{product_code}",
                data=json.dumps(TestUtils.product_data_update),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], f"Product with code: {product_code} does not exist"
            )

    def test_update_product_by_code_invalid_category(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        with self.client:
            response = self.client.put(
                f"/products/code/{product.code}",
                data=json.dumps(TestUtils.product_data_invalid_category),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"], "Sorry. This product category does not exist"
            )

    def test_update_product_by_code_company_missing(self):
        product = TestUtils.add_product(**TestUtils.product_data)
        new_data = dict(**TestUtils.product_data)
        new_data.pop("company")
        with self.client:
            response = self.client.put(
                f"/products/code/{product.code}",
                data=json.dumps(new_data),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                f"Invalid Payload. Mandatory field 'company' is missing",
            )

    def test_update_product_by_code_duplicate_name(self):
        product_1 = TestUtils.add_product(**TestUtils.product_data)
        product_2 = TestUtils.add_product(**TestUtils.product_data_update)
        with self.client:
            response = self.client.put(
                f"/products/code/{product_2.code}",
                data=json.dumps({"name": product_1.name, "company": product_1.company}),
                content_type="application/json",
                headers=dict(Authorization=f"Bearer {self.AUTH_TOKEN}"),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertRegex(data["message"], "^Product with Key.*already exists.")


if __name__ == "__main__":
    unittest.main()
