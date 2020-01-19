# services/users/project/api/views/test_utils.py

from functools import wraps
from flask import request, jsonify

from project import db
from project.api.models.addresses import AddressModel
from project.api.models.companies import CompanyModel, CompanyType
from project.api.models.retailers import RetailerModel
from project.api.models.stores import StoreModel, StoreType
from project.api.models.suppliers import SupplierModel
from project.api.models.users import UserModel, UserType


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {"status": "fail", "message": "Provide a valid auth token."}
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return response_object, 403
        auth_token = auth_header.split(" ")[1]
        resp = UserModel.decode_token(auth_token)
        if isinstance(resp, str):
            response_object["message"] = resp
            return response_object, 401
        user = UserModel.find_by_id(_id=resp)
        if not user:
            return response_object, 401
        confirmation = user.most_recent_confirmation
        if not confirmation or not confirmation.confirmed:
            response_object[
                "message"
            ] = "You have not confirmed registration. Please check your email."
            return response_object, 401
        return f(resp, *args, **kwargs)

    return decorated_function


def is_admin(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return user.admin


def add_user_to_db(
    username, password, email, user_type, street_name, street_number, city, zip_code
):
    new_user = UserModel(
        username=username, password=password, email=email, user_type=user_type
    )
    db.session.add(new_user)
    # add address
    new_address = AddressModel(
        street_name=street_name,
        street_number=street_number,
        city=city,
        zip_code=zip_code,
    )
    db.session.add(new_address)
    db.session.commit()
    return new_user, new_address


def add_retail_user_to_db(
    username,
    password,
    email,
    street_name,
    street_number,
    city,
    zip_code,
    store_name,
    store_type,
):
    if store_type not in set(item.name for item in StoreType):
        raise ValueError
    # add new retail user to db
    new_user, new_address = add_user_to_db(
        username=username,
        password=password,
        email=email,
        user_type=UserType.retail.name,
        street_name=street_name,
        street_number=street_number,
        city=city,
        zip_code=zip_code,
    )
    # add retailer
    new_retailer = RetailerModel(user_id=new_user.id)
    db.session.add(new_retailer)
    db.session.commit()
    store = StoreModel(
        retailer_id=new_retailer.id,
        store_name=store_name,
        store_type=store_type,
        address_id=new_address.id,
    )
    db.session.add(store)
    db.session.commit()

    return new_user


def add_wholesale_user_to_db(
    username,
    password,
    email,
    street_name,
    street_number,
    city,
    zip_code,
    company_name,
    company_type,
):
    if company_type not in set(item.name for item in CompanyType):
        raise ValueError
    # add new wholesale user to db
    new_user, new_address = add_user_to_db(
        username=username,
        password=password,
        email=email,
        user_type=UserType.wholesale.name,
        street_name=street_name,
        street_number=street_number,
        city=city,
        zip_code=zip_code,
    )
    # add supplier
    new_supplier = SupplierModel(user_id=new_user.id)
    db.session.add(new_supplier)
    db.session.commit()
    company = CompanyModel(
        supplier_id=new_supplier.id,
        company_name=company_name,
        company_type=company_type,
        address_id=new_address.id,
    )
    db.session.add(company)
    db.session.commit()

    return new_user
