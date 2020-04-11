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
    image = db.Column(db.String(255), unique=False, nullable=True)
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
            "category": self.category.name,
            "quantity": self.quantity,
            "image": self.image,
        }

    @classmethod
    def find_by_id(cls, _id: int) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, product_name: str) -> "ProductModel":
        return cls.query.filter_by(name=product_name).first()

    @classmethod
    def find_by_code(cls, product_code: str) -> "ProductModel":
        return cls.query.filter_by(code=product_code).first()

    @classmethod
    def already_exists(cls, name: str, code: str) -> bool:
        return (
            (
                cls.query.filter_by(name=name).first()
                or cls.query.filter_by(code=code).first()
            )
            and True
            or False
        )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self, data: Dict) -> None:
        self.code = data["code"] if "code" in data else self.code
        self.name = data["name"] if "name" in data else self.name
        self.category_id = (
            data["category_id"] if "category_id" in data else self.category_id
        )
        self.quantity = data["quantity"] if "quantity" in data else self.quantity
        self.image = data["image"] if "image" in data else self.image
        db.session.commit()
