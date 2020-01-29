# project/api/models/product_categories.py


from typing import Dict
from project import db


class ProductCategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, description):
        self.description = description

    def json(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
        }

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductCategoryModel":
        return cls.query.filter_by(id=_id).first()
