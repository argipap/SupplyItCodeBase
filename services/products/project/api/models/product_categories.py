# project/api/models/product_categories.py


from typing import Dict
from project import db


class ProductCategoryModel(db.Model):

    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
        }

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductCategoryModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_category_id_by_name(cls, category_name) -> "ProductCategoryModel":
        return cls.query.filter_by(name=category_name).first().id
