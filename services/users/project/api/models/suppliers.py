# project/api/models/suppliers.py

from project import db
from project.api.models.association_tables import retailers_to_suppliers


class SuppliersModel(db.Model):

    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
