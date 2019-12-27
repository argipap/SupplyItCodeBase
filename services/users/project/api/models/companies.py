# project/api/models/companies.py

from project import db
import enum


class CompanyType(enum.Enum):
    other = 1
    meat_and_poultry = 2
    coffee_and_drinks = 3


class CompanyModel(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    company_address = db.relationship("AddressModel", backref="company", uselist=False)
    address_id = db.Column(
        db.Integer, db.ForeignKey("addresses.id"), unique=True, nullable=False
    )
    company_type = db.Column(
        db.Enum(CompanyType), default=CompanyType.other, nullable=False
    )

    def __init__(
        self, supplier_id, company_name, address_id, company_type=CompanyType.other
    ):
        self.supplier_id = supplier_id
        self.company_name = (company_name,)
        self.company_type = company_type
        self.address_id = address_id

    def json(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "company_name": self.company_name,
            "company_type": self.company_type.name,
            "address_id": self.address_id,
        }
