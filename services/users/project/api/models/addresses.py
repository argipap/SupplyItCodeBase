# project/api/models/addresses.py

from project import db


class AddressModel(db.Model):
    # concatenation of streetName streetNumber, City, zipCode
    # e.g Aigaiou 46, Rafina 19009

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_name = db.Column(db.String(128), nullable=False)
    street_number = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(50), nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=True, nullable=True
    )
    company_id = db.Column(
        db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=True
    )

    def __repr__(self):
        return f"{self.street_name} {self.street_number}, {self.city} {self.zip_code}"

    def __init__(
        self, street_name, street_number, city, zip_code, store_id=None, company_id=None
    ):
        self.street_name = street_name
        self.street_number = street_number
        self.city = city
        self.zip_code = zip_code
        self.store_id = store_id
        self.company_id = company_id

    def json(self):
        return {
            "id": self.id,
            "street_name": self.street_name,
            "street_number": self.street_number,
            "city": self.city,
            "zip_code": self.zip_code,
        }
