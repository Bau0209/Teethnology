from app import db

class InventoryUsage(db.Model):
    __tablename__ = "inventory_usage"

    id = db.Column(db.Integer, primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey("procedure_history.procedure_id"), nullable=False)
    inventory_item_id = db.Column(db.String(10), db.ForeignKey("inventory_items.item_id"), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)

    procedure = db.relationship("Procedures", backref="inventory_usages")
    inventory_item = db.relationship("InventoryItem", backref="usages")
