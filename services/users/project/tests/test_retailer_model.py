# services/users/project/tests/test_retailer_model.py


import unittest

from project import db
from project.api.models.retailers import RetailerModel
from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils


from sqlalchemy.exc import IntegrityError


class TestRetailerModel(BaseTestCase):
    def test_add_retailer(self):
        # first add a retail user
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        self.assertTrue(retailer.id)
        self.assertEqual(user.id, retailer.id)

    def test_add_retailer_with_invalid_uid(self):
        """
        A retailer should have a user_id which is present on users table.
        Test is to confirm that integrity db error (ForeignKeyViolation) will be raised
        in case of no user.
        """
        retailer = RetailerModel(user_id=999)
        db.session.add(retailer)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_retailer_duplicate_user(self):
        user = TestUtils.add_user(**TestData.retailer_data_model)
        TestUtils.add_retailer(user.id)
        duplicate_retailer = RetailerModel(user_id=user.id)
        db.session.add(duplicate_retailer)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        self.assertTrue(isinstance(retailer.json(), dict))


if __name__ == "__main__":
    unittest.main()
