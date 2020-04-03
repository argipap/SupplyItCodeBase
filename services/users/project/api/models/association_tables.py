from project import db

retailers_to_suppliers = db.Table(
    "retailers_to_suppliers",
    db.Column("supplier_id", db.Integer, db.ForeignKey("suppliers.id")),
    db.Column("retailer_id", db.Integer, db.ForeignKey("retailers.id")),
)
