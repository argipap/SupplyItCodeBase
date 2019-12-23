# project/api/models/stores.py

from project import db
import enum


class StoreType(enum.Enum):
    other = 1
    cafeBar = 2
    restaurant = 3
    quick_service_restaurant = 4


class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey("retailers.id"), nullable=False)
    store_name = db.Column(db.String(128), nullable=False)
    store_address = db.relationship("AddressModel", backref="store", uselist=False)
    store_type = db.Column(db.Enum(StoreType), default=StoreType.other, nullable=False)

    def __init__(self, retailer_id, store_name, store_type):
        self.retailer_id = retailer_id
        self.store_name = store_name
        self.store_type = store_type

    def json(self):
        return {
            "id": self.id,
            "retailer_id": self.retailer_id,
            "store_name": self.store_name,
            "store_address": self.store_address,
            "store_type": self.store_type,
        }
