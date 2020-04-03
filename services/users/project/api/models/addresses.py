# project/api/models/addresses.py

from project import db


class AddressModel(db.Model):

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_name = db.Column(db.String(128), nullable=False)
    street_number = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(50), nullable=False)

    def __init__(self, street_name, street_number, city, zip_code):
        self.street_name = street_name
        self.street_number = street_number
        self.city = city
        self.zip_code = zip_code

    def __repr__(self):
        return f"{self.street_name} {self.street_number}, {self.city} {self.zip_code}"

    def json(self):
        return {"address": self.__repr__()}
