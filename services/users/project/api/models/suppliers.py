# project/api/models/suppliers.py

from project import db


class SupplierModel(db.Model):

    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    companies = db.relationship("CompanyModel", backref="supplier")

    def __init__(self, user_id):
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "user_id": self.user_id}
