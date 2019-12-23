# project/api/models/companies.py

from project import db
import enum


class SupplyType(enum.Enum):
    other = 1
    meat_and_poultry = 2
    drinks = 3
    coffee = 4


class CompanyModel(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    company_address = db.relationship("AddressModel", backref="company", uselist=False)
    supply_type = db.Column(
        db.Enum(SupplyType), default=SupplyType.other, nullable=False
    )

    def __init__(self, supplier_id, company_name, supply_type):
        self.supplier_id = supplier_id
        self.company_name = (company_name,)
        self.supply_type = supply_type

    def json(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "company_name": self.company_name,
            "company_address": self.company_address,
            "supply_type": self.supply_type,
        }
