from app.models import InventoryUsage, InventoryItem
from app import db

def create_inventory_usage_record(procedure_id, inventory_item_id, quantity_used):
     # Create the usage record
    inventory_usage = InventoryUsage(
        procedure_id=procedure_id,
        inventory_item_id=inventory_item_id,
        quantity_used=quantity_used
    )
    db.session.add(inventory_usage)

    # Deduct from the inventory
    inventory_item = InventoryItem.query.get(inventory_item_id)
    if inventory_item:
        new_quantity = float(inventory_item.quantity) - float(quantity_used)
        inventory_item.quantity = max(new_quantity, 0)  # Avoid negative stock

    # Commit everything
    db.session.commit()
