# project/api/models/products.py

from typing import Dict, List
from datetime import datetime
from project import db


class ProductModel(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    code = db.Column(db.String(255), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_categories.id"), nullable=False
    )
    category = db.relationship("ProductCategoryModel", backref="product")
    image = db.Column(db.String(255), unique=False, nullable=True)
    company = db.Column(db.String(255), unique=False, nullable=False)
    added_by = db.Column(db.String(255), unique=False, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    __table_args__ = (
        db.Index("company_name_index", "company", "name", unique=True),
        db.Index("company_code_index", "company", "code", unique=True),
    )

    def __init__(
        self,
        name: str,
        code: str,
        category_id: int,
        company: str,
        added_by: str,
        quantity: str = 1,
        image: str = None,
    ):
        self.name = name
        self.code = code
        self.category_id = category_id
        self.quantity = quantity
        self.company = company
        self.added_by = added_by
        self.image = image

    def json(self) -> Dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category.name,
            "quantity": self.quantity,
            "image": self.image,
            "company": self.company,
            "added_by": self.added_by,
        }

    @classmethod
    def find_by_id(cls, _id: int) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_company(cls, company: str) -> List["ProductModel"]:
        return [product.json() for product in cls.query.filter_by(company=company)]

    @classmethod
    def find_by_name(cls, product_name: str) -> List["ProductModel"]:
        return [product.json() for product in cls.query.filter_by(name=product_name)]

    @classmethod
    def find_by_name_and_company(
        cls, product_name: str, company: str
    ) -> "ProductModel":
        return cls.query.filter_by(name=product_name, company=company).first()

    @classmethod
    def find_by_code(cls, product_code: str) -> List["ProductModel"]:
        return [product.json() for product in cls.query.filter_by(code=product_code)]

    @classmethod
    def find_by_code_and_company(
            cls, product_code: str, company: str
    ) -> "ProductModel":
        return cls.query.filter_by(code=product_code, company=company).first()

    @classmethod
    def already_exists(cls, name: str, code: str, company: str) -> bool:
        return (
            (
                cls.query.filter_by(name=name, company=company).first()
                or cls.query.filter_by(code=code, company=company).first()
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
