# project/api/models/retailers.py

from project import db
from project.api.models.association_tables import retailers_to_suppliers


class RetailersModel(db.Model):

    __tablename__ = "retailers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    suppliers = db.relationship(
        "SuppliersModel",
        secondary=retailers_to_suppliers,
        backref="retailers",
        lazy="dynamic"
    )
