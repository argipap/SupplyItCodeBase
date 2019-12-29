# project/api/models/retailers.py

from project import db
from project.api.models.association_tables import retailers_to_suppliers


class RetailerModel(db.Model):

    __tablename__ = "retailers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    stores = db.relationship(
        "StoreModel", backref="retailer", lazy="dynamic", cascade="all, delete-orphan"
    )
    suppliers = db.relationship(
        "SupplierModel",
        secondary=retailers_to_suppliers,
        backref="retailers",
        lazy="dynamic"
    )

    def __init__(self, user_id):
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "user_id": self.user_id}
