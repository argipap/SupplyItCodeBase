# project/tests/test_product_category_model.py

import unittest

from project.api.models.product_categories import ProductCategoryModel
from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProductCategoryModel(BaseTestCase):
    def test_deserialization(self):
        product_category = TestUtils.add_product_category("test_category")
        self.assertTrue(isinstance(product_category.json(), dict))
        self.assertEqual(
            product_category.json(),
            {
                "id": product_category.id,
                "name": product_category.name,
            },
        )

    def test_find_by_id(self):
        new_product = TestUtils.add_product_category("test_category")
        self.assertTrue(ProductCategoryModel.find_by_id(new_product.id))

    def test_find_id_by_name(self):
        new_product = TestUtils.add_product_category("test_category")
        self.assertEqual(
            new_product.id,
            ProductCategoryModel.find_by_category(new_product.name).id,
        )


if __name__ == "__main__":
    unittest.main()
