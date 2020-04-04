from project import db
from project.api.models.products import ProductModel


class TestUtils:
    product_data = {
        "name": "test_product",
        "category_id": 2,
        "code": "52",
    }

    @classmethod
    def add_product(cls, name, code, category_id):
        product = ProductModel(name=name, code=code, category_id=category_id)
        db.session.add(product)
        db.session.commit()
        return product
