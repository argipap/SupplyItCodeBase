from project import db
from project.api.models.products import ProductModel


class TestUtils:
    product_data = {
        "name": "test_product",
        "quantity": 3,
        "category_id": 2,
    }

    @classmethod
    def add_product(cls, name, quantity, category_id):
        product = ProductModel(name, quantity, category_id)
        db.session.add(product)
        db.session.commit()
        return product
