# project/tests/test_product_model.py

import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models.products import ProductModel
from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProductModel(BaseTestCase):
    def test_add_product(self):
        new_product = TestUtils.add_product(**TestUtils.product_data)
        self.assertTrue(new_product.id)
        self.assertEqual(new_product.name, "test_product")
        self.assertEqual(new_product.quantity, 1)
        self.assertEqual(new_product.code, TestUtils.product_data["code"])
        self.assertEqual(new_product.category_id, TestUtils.product_data["category_id"])
        self.assertTrue(new_product.date_added, True)
        self.assertFalse(new_product.date_updated, None)

    def test_add_product_with_quantity_and_image(self):
        data = dict(**TestUtils.product_data)
        data["image"] = "test_image.png"
        data["quantity"] = 3
        new_product = TestUtils.add_product(**data)
        self.assertTrue(new_product.id)
        self.assertEqual(new_product.name, "test_product")
        self.assertEqual(new_product.quantity, 3)
        self.assertEqual(new_product.code, data["code"])
        self.assertEqual(new_product.image, data["image"])
        self.assertEqual(new_product.category_id, data["category_id"])

    def test_add_product_duplicate_code(self):
        TestUtils.add_product(**TestUtils.product_data)
        new_data = dict(**TestUtils.product_data)
        new_data["name"] = "new_product"
        duplicate_product = ProductModel(**TestUtils.product_data)
        db.session.add(duplicate_product)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_product_duplicate_name(self):
        TestUtils.add_product(**TestUtils.product_data)
        new_data = dict(**TestUtils.product_data)
        new_data["code"] = 999
        duplicate_product = ProductModel(**TestUtils.product_data)
        db.session.add(duplicate_product)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        new_product = TestUtils.add_product(**TestUtils.product_data)
        self.assertTrue(isinstance(new_product.json(), dict))
        self.assertEqual(
            new_product.json(),
            {
                "id": new_product.id,
                "code": new_product.code,
                "name": new_product.name,
                "category_id": new_product.category_id,
                "quantity": new_product.quantity,
                "image": new_product.image,
            },
        )

    def test_find_by_id(self):
        new_product = TestUtils.add_product(**TestUtils.product_data)
        self.assertTrue(ProductModel.find_by_id(new_product.id))

    def test_find_id_by_name(self):
        new_product = TestUtils.add_product(**TestUtils.product_data)
        self.assertEqual(
            new_product.id, ProductModel.get_product_id_by_name(new_product.name)
        )


if __name__ == "__main__":
    unittest.main()
