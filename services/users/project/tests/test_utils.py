import json

from project.api.models.addresses import AddressModel
from project.api.models.companies import CompanyModel, CompanyType
from project.api.models.retailers import RetailerModel
from project.api.models.suppliers import SupplierModel
from project.api.models.stores import StoreModel, StoreType
from project.api.models.users import UserModel
from project import db


class TestUtils:
    @classmethod
    def user_login(cls, user_data, client):
        cls.add_user(**user_data)
        user = UserModel.query.filter_by(email=user_data["email"]).first()
        user.admin = True
        user.active = True
        db.session.commit()
        resp_login = client.post(
            "/auth/login",
            data=json.dumps(
                {"email": user_data["email"], "password": user_data["password"]}
            ),
            content_type="application/json",
        )
        token = json.loads(resp_login.data.decode())["auth_token"]
        return token

    @classmethod
    def add_user(cls, username, email, password, user_type=None):
        user = UserModel(
            username=username, email=email, password=password, user_type=user_type
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def add_retailer(cls, user_id):
        retailer = RetailerModel(user_id)
        db.session.add(retailer)
        db.session.commit()
        return retailer

    @classmethod
    def add_supplier(cls, user_id):
        supplier = SupplierModel(user_id)
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @classmethod
    def add_address(cls, street_name, street_number, city, zip_code):
        address = AddressModel(
            street_name=street_name,
            street_number=street_number,
            city=city,
            zip_code=zip_code,
        )
        db.session.add(address)
        db.session.commit()
        return address

    @classmethod
    def add_store(
        cls, retailer_id, store_name, address_id, store_type=StoreType.cafeBar
    ):
        supplier = StoreModel(
            retailer_id=retailer_id,
            store_name=store_name,
            store_type=store_type,
            address_id=address_id,
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @classmethod
    def add_company(
        cls,
        supplier_id,
        company_name,
        address_id,
        company_type=CompanyType.meat_and_poultry,
    ):
        company = CompanyModel(
            supplier_id=supplier_id,
            company_name=company_name,
            company_type=company_type,
            address_id=address_id,
        )
        db.session.add(company)
        db.session.commit()
        return company
