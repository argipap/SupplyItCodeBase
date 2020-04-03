# services/users/project/tests/test_supplier_model.py


import unittest

from project import db
from project.api.models.suppliers import SupplierModel
from project.tests.base import BaseTestCase

from sqlalchemy.exc import IntegrityError

from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


class TestSupplierModel(BaseTestCase):
    def test_add_supplier(self):
        # first add a wholesale user
        user = TestUtils.add_user(**TestData.supplier_data_model)
        supplier = TestUtils.add_supplier(user.id)
        self.assertTrue(supplier.id)
        self.assertEqual(user.id, supplier.id)

    def test_add_supplier_with_invalid_uid(self):
        """
        A supplier should have a user_id which is present on users table.
        Test is to confirm that integrity db error (ForeignKeyViolation) will be raised
        in case of no user.
        """
        supplier = SupplierModel(user_id=999)
        db.session.add(supplier)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_supplier_duplicate_user(self):
        user = TestUtils.add_user(**TestData.supplier_data_model)
        TestUtils.add_supplier(user.id)
        duplicate_supplier = SupplierModel(user_id=user.id)
        db.session.add(duplicate_supplier)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestUtils.add_user(**TestData.supplier_data_model)
        supplier = TestUtils.add_supplier(user.id)
        self.assertTrue(isinstance(supplier.json(), dict))


if __name__ == "__main__":
    unittest.main()
