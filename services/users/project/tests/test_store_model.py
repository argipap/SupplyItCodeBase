# services/users/project/tests/test_store_model.py
import json
import unittest

from project import db
from project.api.models.stores import StoreModel
from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils

from sqlalchemy.exc import IntegrityError


class TestStoreModel(BaseTestCase):
    def test_add_store(self):
        # first we should create a user, retailer and address objects
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        store = TestUtils.add_store(
            retailer_id=retailer.id, store_name="TestStore", address_id=address.id
        )
        self.assertTrue(store.id)
        self.assertEqual(user.id, retailer.id)
        self.assertEqual(retailer.id, store.retailer_id)
        self.assertEqual(address.id, store.address_id)

    def test_add_store_with_invalid_retailer(self):
        """Test is to confirm that integrity db error (ForeignKeyViolation) will be raised"""
        address = TestUtils.add_address(**TestData.address_data)
        store = StoreModel(
            retailer_id=999, store_name="TestStore", address_id=address.id
        )
        db.session.add(store)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_store_with_invalid_address(self):
        """Test is to confirm that integrity db error (ForeignKeyViolation) will be raised"""
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        store = StoreModel(
            retailer_id=retailer.id, store_name="TestStore", address_id=999
        )
        db.session.add(store)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_store_duplicate_address(self):
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        TestUtils.add_store(
            retailer_id=retailer.id, store_name="TestStore", address_id=address.id
        )
        duplicate_store_address = StoreModel(
            retailer_id=retailer.id, store_name="TestStore2", address_id=address.id
        )
        db.session.add(duplicate_store_address)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestUtils.add_user(**TestData.retailer_data_model)
        retailer = TestUtils.add_retailer(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        store = TestUtils.add_store(
            retailer_id=retailer.id, store_name="TestStore", address_id=address.id
        )
        self.assertTrue(isinstance(store.json(), dict))


if __name__ == "__main__":
    unittest.main()
