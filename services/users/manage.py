# services/users/manage.py
import os
import sys
import unittest
import coverage

from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models.confirmations import ConfirmationModel
from project.api.models.users import UserModel, UserType
from project.api.models.retailers import RetailerModel
from project.api.models.suppliers import SupplierModel
from project.api.models.stores import StoreModel, StoreType
from project.api.models.companies import CompanyModel, CompanyType
from project.api.models.addresses import AddressModel
from tasks import celery_app
from celery.bin import worker

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py"]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    user_1_s = UserModel(
        username="user_1",
        email="user_1@gmail.com",
        password="supplyit",
        admin=True,
        user_type=UserType.wholesale,
    )
    db.session.add(user_1_s)
    db.session.commit()
    user_2_s = UserModel(
        username="user_2",
        email="user_2@gmail.com",
        password="supplyit",
        user_type=UserType.wholesale,
    )
    db.session.add(user_2_s)
    user_3_r = UserModel(
        username="user_3", email="user_3@gmail.com", password="supplyit"
    )
    db.session.add(user_3_r)
    user_4_r = UserModel(
        username="user_4", email="user_4@gmail.com", password="supplyit"
    )
    db.session.add(user_4_r)
    db.session.commit()

    confirmation_1 = ConfirmationModel(user_1_s.id, confirmed=True)
    confirmation_1.save_to_db()
    confirmation_2 = ConfirmationModel(user_2_s.id, confirmed=True)
    confirmation_2.save_to_db()
    confirmation_3 = ConfirmationModel(user_3_r.id, confirmed=True)
    confirmation_3.save_to_db()
    confirmation_4 = ConfirmationModel(user_4_r.id, confirmed=True)
    confirmation_4.save_to_db()

    # add suppliers
    supplier_1 = SupplierModel(user_id=user_1_s.id)
    db.session.add(supplier_1)
    supplier_2 = SupplierModel(user_id=user_2_s.id)
    db.session.add(supplier_2)

    # add retailers
    retailer_1 = RetailerModel(user_id=user_3_r.id)
    db.session.add(retailer_1)
    retailer_2 = RetailerModel(user_id=user_4_r.id)
    db.session.add(retailer_2)

    retailer_1.suppliers.append(supplier_1)
    retailer_1.suppliers.append(supplier_2)
    retailer_2.suppliers.append(supplier_2)

    db.session.commit()

    # add addresses
    address_1 = AddressModel(
        street_name="Agaiou", street_number="46", city="Rafina", zip_code="190 09",
    )
    db.session.add(address_1)
    address_2 = AddressModel(
        street_name="Στρ. Νικ. Πλαστήρα",
        street_number="ΠΛΑΤΕΙΑ",
        city="Ραφηνα",
        zip_code="190 09",
    )
    db.session.add(address_2)
    address_3 = AddressModel(
        street_name="Dimarchou Christou Mpeka",
        street_number="8",
        city="Spata",
        zip_code="190 04",
    )
    db.session.add(address_3)
    address_4 = AddressModel(
        street_name="Thessalonikis",
        street_number="119",
        city="Athens",
        zip_code="118 52",
    )
    db.session.add(address_4)
    address_5 = AddressModel(
        street_name="Τρωων", street_number="115", city="Athens", zip_code="118 52",
    )
    db.session.add(address_5)
    address_6 = AddressModel(
        street_name="Τρωων", street_number="125", city="Athens", zip_code="118 52",
    )
    db.session.add(address_6)
    # commit for addresses
    db.session.commit()

    # add stores
    store_1 = StoreModel(
        retailer_id=retailer_1.id,
        store_name="store_1",
        store_type=StoreType.cafeBar.name,
        address_id=address_4.id,
    )
    db.session.add(store_1)
    store_2 = StoreModel(
        retailer_id=retailer_2.id,
        store_name="store_2",
        store_type=StoreType.quick_service_restaurant.name,
        address_id=address_5.id,
    )
    db.session.add(store_2)
    store_3 = StoreModel(
        retailer_id=retailer_2.id,
        store_name="store_3",
        store_type=StoreType.other.name,
        address_id=address_6.id,
    )
    db.session.add(store_3)

    # add companies
    company_1 = CompanyModel(
        supplier_id=supplier_1.id,
        company_name="company_1",
        address_id=address_1.id,
        company_type=CompanyType.meat_and_poultry,
    )
    db.session.add(company_1)

    company_2 = CompanyModel(
        supplier_id=supplier_1.id,
        company_name="company_2",
        company_type=CompanyType.meat_and_poultry,
        address_id=address_2.id,
    )
    db.session.add(company_2)
    company_3 = CompanyModel(
        supplier_id=supplier_2.id,
        company_name="company_3",
        company_type=CompanyType.coffee_and_drinks,
        address_id=address_3.id,
    )
    db.session.add(company_3)

    db.session.commit()


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
