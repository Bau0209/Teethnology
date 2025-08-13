from datetime import date
from app import db
from sqlalchemy import func
from app.models import (
    InventoryItem,
    InventoryConsumable,
    InventoryMedication,
    InventoryLabMaterial,
    InventorySterilization
)

def get_inventory_report_data(selected_branch="all"):
    today = date.today()

    # Base query
    base_query = InventoryItem.query
    if selected_branch != "all":
        base_query = base_query.filter(InventoryItem.branch_id == selected_branch)

    # Queries for each category
    consumable_query = db.session.query(InventoryConsumable).join(InventoryItem)
    medication_query = db.session.query(InventoryMedication).join(InventoryItem)
    lab_material_query = db.session.query(InventoryLabMaterial).join(InventoryItem)
    sterilization_query = db.session.query(InventorySterilization).join(InventoryItem)

    if selected_branch != "all":
        consumable_query = consumable_query.filter(InventoryItem.branch_id == selected_branch)
        medication_query = medication_query.filter(InventoryItem.branch_id == selected_branch)
        lab_material_query = lab_material_query.filter(InventoryItem.branch_id == selected_branch)
        sterilization_query = sterilization_query.filter(InventoryItem.branch_id == selected_branch)

    # Counts for low stock, out of stock, expired
    low_stock_count = (
        consumable_query.filter(InventoryConsumable.stock_status == 'low stock').count() +
        medication_query.filter(InventoryMedication.stock_status == 'low stock').count() +
        lab_material_query.filter(InventoryLabMaterial.stock_status == 'low stock').count() +
        sterilization_query.filter(InventorySterilization.stock_status == 'low stock').count()
    )

    out_of_stock_count = (
        consumable_query.filter(InventoryConsumable.stock_status == 'out of stock').count() +
        medication_query.filter(InventoryMedication.stock_status == 'out of stock').count() +
        lab_material_query.filter(InventoryLabMaterial.stock_status == 'out of stock').count() +
        sterilization_query.filter(InventorySterilization.stock_status == 'out of stock').count()
    )

    expired_count = (
        consumable_query.filter(InventoryConsumable.expiration_date < today).count() +
        medication_query.filter(InventoryMedication.expiration_date < today).count() +
        lab_material_query.filter(InventoryLabMaterial.expiration_date < today).count() +
        sterilization_query.filter(InventorySterilization.expiration_date < today).count()
    )

    # Inventory vs Consumption - estimate consumption based on minimum stock
    inventory_items = base_query.with_entities(
        InventoryItem.item_name,
        InventoryItem.quantity,
        InventoryItem.category
    ).all()

    estimated_consumption = []
    for item_name, quantity, category in inventory_items:
        # Estimate usage: if minimum stock exists, assume it’s monthly usage
        min_stock = 0
        if category == "consumable":
            c = InventoryConsumable.query.join(InventoryItem).filter(InventoryItem.item_name == item_name).first()
            if c and c.minimum_stock:
                min_stock = c.minimum_stock
        elif category == "medication":
            m = InventoryMedication.query.join(InventoryItem).filter(InventoryItem.item_name == item_name).first()
            if m and m.minimum_stock:
                min_stock = m.minimum_stock
        elif category == "lab_material":
            l = InventoryLabMaterial.query.join(InventoryItem).filter(InventoryItem.item_name == item_name).first()
            if l and l.minimum_stock:
                min_stock = l.minimum_stock
        elif category == "sterilization":
            s = InventorySterilization.query.join(InventoryItem).filter(InventoryItem.item_name == item_name).first()
            if s and s.minimum_stock_level:
                min_stock = s.minimum_stock_level

        # If no min stock info, just use 30% of current quantity
        if min_stock == 0:
            estimated_consumption.append(round(quantity * 0.3, 2))
        else:
            estimated_consumption.append(round(min_stock, 2))

    inventory_vs_consumption = {
        "labels": [i[0] for i in inventory_items],
        "inventory": [i[1] for i in inventory_items],
        "consumption": estimated_consumption
    }

    # Supply use per "service" - group by category instead
    category_usage = {}
    for (item_name, quantity, category), consumption in zip(inventory_items, estimated_consumption):
        category_usage.setdefault(category, 0)
        category_usage[category] += consumption

    supply_use_per_service = {
        "labels": list(category_usage.keys()),
        "data": list(category_usage.values())
    }

    return {
        "low_stock": low_stock_count,
        "out_of_stock": out_of_stock_count,
        "expired": expired_count,
        "inventory_vs_consumption": inventory_vs_consumption,
        "supply_use_per_service": supply_use_per_service
    }
