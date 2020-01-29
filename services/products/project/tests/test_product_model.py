# project/tests/test_product_model.py

import unittest

from project.tests.test_base import BaseTestCase
from project.tests.utils import TestUtils


class TestProductModel(BaseTestCase):
    def test_add_product(self):
        new_product = TestUtils.add_product(**TestUtils.product_data)
        self.assertTrue(new_product.id)
        self.assertEqual(new_product.name, "test_product")
        self.assertEqual(new_product.quantity, 3)


if __name__ == "__main__":
    unittest.main()
