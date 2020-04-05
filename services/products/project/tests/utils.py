import json
import requests

from flask import current_app

from project.api.models.product_categories import ProductCategoryModel
from project.api.models.products import ProductModel
import mailslurp_client
from mailslurp_client.rest import ApiException


class TestUtils:
    USERS_DOMAIN = current_app.config["USERS_SERVICE_URL"]
    MAILSLURP_API_KEY = current_app.config["MAILSLURP_API_KEY"]
    INBOX_ID = "01802e18-bc17-42fb-ac23-fe09814aaaf3"

    product_data = {
        "name": "test_product",
        "category_id": 2,
        "code": "52",
    }

    user_data_retail = {
        "username": "testuser",
        "email": f"{INBOX_ID}@mailslurp.com",
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
    def add_product(cls, name, code, category_id, quantity=None, image=None):
        product = ProductModel(
            name=name,
            code=code,
            category_id=category_id,
            quantity=quantity,
            image=image,
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
        requests.delete(
            f"{cls.USERS_DOMAIN}/users/email/{email}", headers=headers,
        )

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
            return False

    @classmethod
    def confirm_user(cls):
        """need to make an {USERS_DOMAIN}/auth/confirmation/<uuid> request"""
        # using Mailslurp client to  mock. First empty inbox from mails
        mailslurp_config = cls.mailslurp_configuration()
        cls.mailslurp_empty_inbox(mailslurp_config)
        # but first we need to send/receive a fake email using MAILSLURP
        confirmation_id = (
            cls.mailslurp_wait_for_latest_email(mailslurp_config)
            .body.split("=")[1]
            .split(">")[0]
            .split("/")[-1]
        )
        headers = {"content_type": "application/json"}
        print(f"{cls.USERS_DOMAIN}/auth/confirmation/{confirmation_id}")
        response = requests.get(
            f"{cls.USERS_DOMAIN}/auth/confirmation/{confirmation_id}", headers=headers,
        )
        print(response.status_code)
        if response.status_code == 200:
            return True
        return False

    @classmethod
    def mailslurp_configuration(cls):
        configuration = mailslurp_client.Configuration()
        # Configure API key authorization: API_KEY
        configuration.api_key["x-api-key"] = TestUtils.MAILSLURP_API_KEY
        return configuration

    @classmethod
    def mailslurp_wait_for_latest_email(cls, configuration):
        with mailslurp_client.ApiClient(configuration) as api_client:
            api_instance = mailslurp_client.WaitForControllerApi(api_client)
            inbox_id = TestUtils.INBOX_ID
            timeout = 5000
            try:
                api_response = api_instance.wait_for_latest_email(
                    inbox_id=inbox_id, timeout=timeout, unread_only=False
                )
                return api_response
            except ApiException as e:
                print(
                    "Exception calling WaitForControllerApi->wait_for_latest_email: %s"
                    % e
                )
        return False

    @classmethod
    def mailslurp_empty_inbox(cls, configuration):
        with mailslurp_client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = mailslurp_client.CommonActionsControllerApi(api_client)

            try:
                # Delete all emails in an inbox
                api_instance.empty_inbox(cls.INBOX_ID)
            except ApiException as e:
                print(
                    "Exception calling CommonActionsControllerApi->empty_inbox: %s" % e
                )
