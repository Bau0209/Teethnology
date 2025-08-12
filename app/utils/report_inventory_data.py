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

# If you have an AppointmentService or ServiceUsage table that links inventory usage to services,
# replace the dummy logic for "Supply use per service" with real queries.
# For now, it's simulated with random/sample values.

def get_inventory_report_data(selected_branch="all"):
    today = date.today()

    # Base query
    base_query = InventoryItem.query
    if selected_branch != "all":
        base_query = base_query.filter(InventoryItem.branch_id == selected_branch)

    # Join with all categories that have stock_status
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

    # Inventory vs Consumption chart data
    # Here, consumption is a placeholder — you should replace with your actual usage data
    inventory_items = base_query.with_entities(InventoryItem.item_name, InventoryItem.quantity).all()
    inventory_vs_consumption = {
        "labels": [i[0] for i in inventory_items],
        "inventory": [i[1] for i in inventory_items],
        "consumption": [round(i[1] * 0.4, 2) for i in inventory_items]  # Dummy 40% usage
    }

    # Supply use per service chart data (dummy example)
    supply_use_per_service = {
        "labels": ["Cleaning", "Filling", "Extraction", "Braces", "Whitening"],
        "data": [150, 90, 70, 40, 30]
    }

    return {
        "low_stock": low_stock_count,
        "out_of_stock": out_of_stock_count,
        "expired": expired_count,
        "inventory_vs_consumption": inventory_vs_consumption,
        "supply_use_per_service": supply_use_per_service
    }

