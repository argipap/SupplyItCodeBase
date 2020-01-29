# project/api/models/products.py

from typing import Dict
from datetime import datetime
from project import db


class ProductModel(db.Model):

    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    quantity = db.Column(db.Integer, unique=True, nullable=False, default=0)
    category_id = db.Column(
        db.Integer, nullable=False  # db.ForeignKey("product_category.id")
    )
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, name, quantity, category_id):
        self.name = name
        self.quantity = quantity
        self.category_id = category_id

    def json(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "category_id": self.category_id,
        }

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()
