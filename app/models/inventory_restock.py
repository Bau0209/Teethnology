from app import db

class InventoryRestock(db.Model):
    __tablename__ = "inventory_restock"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("inventory_items.item_id"), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.branch_id"), nullable=False)  # ✅ ADD FK
    restock_date = db.Column(db.Date, nullable=False)
    quantity_added = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(255))
    notes = db.Column(db.Text)

    inventory_item = db.relationship("InventoryItem", backref="restocks")
    branch = db.relationship("Branch", backref="restocks")
