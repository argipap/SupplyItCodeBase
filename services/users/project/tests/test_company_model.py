# services/users/project/tests/test_company_model.py


import unittest

from project import db
from project.api.models.companies import CompanyModel
from project.tests.base import BaseTestCase
from project.tests.test_data import TestData
from project.tests.test_utils import TestUtils

from sqlalchemy.exc import IntegrityError


class TestCompanyModel(BaseTestCase):
    def test_add_company(self):
        # first we should create a user, a supplier and an address objects
        user = TestUtils.add_user(**TestData.retailer_data_model)
        supplier = TestUtils.add_supplier(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        company = TestUtils.add_company(
            supplier_id=supplier.id, company_name="TestCompany", address_id=address.id
        )
        self.assertTrue(company.id)
        self.assertEqual(user.id, supplier.id)
        self.assertEqual(supplier.id, company.supplier_id)
        self.assertEqual(address.id, company.address_id)

    def test_add_company_with_invalid_retailer(self):
        """Test is to confirm that integrity db error (ForeignKeyViolation) will be raised"""
        address = TestUtils.add_address(**TestData.address_data)
        company = CompanyModel(
            supplier_id=999, company_name="TestStore", address_id=address.id
        )
        db.session.add(company)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_company_with_invalid_address(self):
        """Test is to confirm that integrity db error (ForeignKeyViolation) will be raised"""
        user = TestUtils.add_user(**TestData.retailer_data_model)
        supplier = TestUtils.add_supplier(user.id)
        company = CompanyModel(
            supplier_id=supplier.id, company_name="TestStore", address_id=999
        )
        db.session.add(company)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_company_duplicate_address(self):
        user = TestUtils.add_user(**TestData.retailer_data_model)
        supplier = TestUtils.add_supplier(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        TestUtils.add_company(
            supplier_id=supplier.id, company_name="TestCompany", address_id=address.id
        )
        duplicate_store_address = CompanyModel(
            supplier_id=supplier.id, company_name="TestStore2", address_id=address.id
        )
        db.session.add(duplicate_store_address)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_deserialization(self):
        user = TestUtils.add_user(**TestData.supplier_data_model)
        supplier = TestUtils.add_supplier(user.id)
        address = TestUtils.add_address(**TestData.address_data)
        company = TestUtils.add_company(
            supplier_id=supplier.id, company_name="TestCompany", address_id=address.id
        )
        self.assertTrue(isinstance(company.json(), dict))


if __name__ == "__main__":
    unittest.main()
