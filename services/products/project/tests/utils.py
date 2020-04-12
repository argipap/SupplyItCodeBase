# project/tests/utils.py


import json
import requests

from flask import current_app

from project.api.models.product_categories import ProductCategoryModel
from project.api.models.products import ProductModel
from project.tests.mailslurp_lib import MailSlurpClient


class TestUtils:
    USERS_DOMAIN = current_app.config["USERS_SERVICE_URL"]

    product_data = {
        "name": "test_product",
        "category": "meat_and_poultry",
        "code": "52",
        "added_by": "user_1@gmail.com",
        "company": "company_1"
    }

    product_data_update = {
        "name": "test_product2",
        "category": "alcohol_and_beverages",
        "code": "53",
        "added_by": "user_1@gmail.com",
        "company": "company_1",
        "image": "update.png",
        "quantity": 100
    }

    product_data_update_invalid_keys = {
        "naasfme": "test_product2",
        "catasdfegory": "alcohol_and_beverages",
        "coadfsde": "53",
        "imasdfage": "update.png",
        "addessd_by": "user_1@gmail.com",
        "company": "company_1",
        "quadsfantity": 100
    }

    product_data_invalid_category = {
        "name": "test_product2",
        "category": "asdfasdfasfa",
        "added_by": "user_1@gmail.com",
        "company": "company_1",
        "code": "53",
        "image": "update.png",
        "quantity": 100
    }

    user_data_retail = {
        "username": "testuser",
        "email": f"{MailSlurpClient.INBOX_ID}@mailslurp.com",
        "password": "123abc!",
        "store_name": "testStore",
        "store_type": "other",
        "street_name": "testStreet",
        "street_number": "testStreetNumber",
        "city": "testCity",
        "zip_code": "testZipCode",
        "user_type": "retail",
    }

    @classmethod
    def add_product(cls, name, code, category, added_by, company, quantity=None, image=None):
        product = ProductModel(
            name=name,
            code=code,
            category_id=ProductCategoryModel.find_by_category(category).id,
            quantity=quantity,
            image=image,
            added_by=added_by,
            company=company,
        )
        product.save_to_db()
        return product

    @classmethod
    def add_product_category(cls, name):
        product_category = ProductCategoryModel(name=name)
        product_category.save_to_db()
        return product_category

    @classmethod
    def user_login(cls, user_data):
        # delete user if exists
        cls.delete_user(user_data["email"])
        # then register user
        cls.register_retail_user(**user_data)
        # then confirm user
        cls.confirm_user()

        headers = {"content_type": "application/json"}
        resp_login = requests.post(
            f"{cls.USERS_DOMAIN}/auth/login",
            data=json.dumps(
                {"email": user_data["email"], "password": user_data["password"]}
            ),
            headers=headers,
        )
        token = json.loads(resp_login.text)["auth_token"]
        return token

    @classmethod
    def delete_user(cls, email):
        headers = {"content_type": "application/json"}
        response = requests.delete(
            f"{cls.USERS_DOMAIN}/users/email/{email}", headers=headers,
        )
        print(f"delete user response: {response.status_code},  {response.text}")

    @classmethod
    def register_retail_user(
        cls,
        username,
        email,
        password,
        store_name,
        store_type,
        street_name,
        street_number,
        city,
        zip_code,
        user_type,
    ):
        """need to make a {USERS_DOMAIN}/auth/register request"""
        headers = {"content_type": "application/json"}
        response = requests.post(
            f"{cls.USERS_DOMAIN}/auth/{user_type}/register",
            data=json.dumps(
                {
                    "email": email,
                    "username": username,
                    "password": password,
                    "store_name": store_name,
                    "store_type": store_type,
                    "street_name": street_name,
                    "street_number": street_number,
                    "city": city,
                    "zip_code": zip_code,
                }
            ),
            headers=headers,
        )
        data = json.loads(response.text)
        if response.status_code == 200 and data["status"] == "success":
            return data
        else:
            return response.text

    @classmethod
    def confirm_user(cls):
        """need to make an {USERS_DOMAIN}/auth/confirmation/<uuid> request"""
        # using Mailslurp client to  mock. First empty inbox from mails
        mailslurp_config = MailSlurpClient.CONFIGURATION
        MailSlurpClient.mailslurp_empty_inbox(mailslurp_config)
        # but first we need to send/receive a fake email using MAILSLURP
        confirmation_id = (
            MailSlurpClient.mailslurp_wait_for_latest_email(mailslurp_config)
            .body.split("=")[1]
            .split(">")[0]
            .split("/")[-1]
        )
        headers = {"content_type": "application/json"}
        print(f"{cls.USERS_DOMAIN}/auth/confirmation/{confirmation_id}")
        response = requests.get(
            f"{cls.USERS_DOMAIN}/auth/confirmation/{confirmation_id}",
            headers=headers,
        )
        print(response.status_code)
        if response.status_code == 200:
            return True
        return False
