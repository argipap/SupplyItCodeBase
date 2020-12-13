# project/tests/base.py


from flask_testing import TestCase
from project import create_app, db
from project.api.models.product_categories import ProductCategoryModel
from project.tests.utils import TestUtils

app = create_app()


class BaseTestCase(TestCase):
    # initialize auth_token by login user with request to users service
    AUTH_TOKEN = TestUtils.user_login(TestUtils.user_data_retail)

    def create_app(self):
        app.config.from_object("project.config.TestingConfig")
        return app

    def setUp(self):
        # create database and tables
        db.create_all()
        # populate product categories
        self.seed_categories()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def seed_categories():
        """Seeds the product_categories table in database."""
        product_categories = [
            "meat_and_poultry",
            "dairy_and_eggs",
            "alcohol_and_beverages",
            "food_and_vegetables",
            "seafood",
        ]
        for category_name in product_categories:
            ProductCategoryModel(name=category_name).save_to_db()
