# project/api/models/products.py

from typing import Dict
from datetime import datetime
from project import db


class ProductModel(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_categories.id"), nullable=False
    )
    category = db.relationship("ProductCategoryModel", backref="product")
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, name, code, category_id, quantity=1, image=None):
        self.name = name
        self.code = code
        self.category_id = category_id
        self.quantity = quantity
        self.image = image

    def json(self) -> Dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category_id": self.category_id,
            "quantity": self.quantity,
            "image": self.image,
        }

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_product_id_by_name(cls, product_name) -> "ProductModel":
        return cls.query.filter_by(name=product_name).first().id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
