from datetime import date
from app import db
from sqlalchemy import func
from app.models import (
    InventoryItem,
    InventoryUsage,
    InventoryRestock,
    InventoryConsumable,
    InventoryMedication,
    InventoryLabMaterial,
    InventorySterilization
)

def get_inventory_report_data(selected_branch="all"):
    today = date.today()

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

    # Main inventory data with usage and restock
    inventory_data = (
        db.session.query(
            InventoryItem.item_name,
            InventoryItem.quantity,
            InventoryItem.category,
            func.COALESCE(func.SUM(InventoryUsage.quantity_used), 0).label("total_usage"),
            func.COALESCE(func.SUM(InventoryRestock.quantity_added), 0).label("total_restock")
        )
        .outerjoin(InventoryUsage, InventoryItem.item_id == InventoryUsage.inventory_item_id)
        .outerjoin(InventoryRestock, InventoryItem.item_id == InventoryRestock.item_id)
        .group_by(
            InventoryItem.item_id,
            InventoryItem.item_name,
            InventoryItem.quantity,
            InventoryItem.category
        )
        .all()
    )

    # Prepare chart/data output
    inventory_vs_consumption = {
        "labels": [row.item_name for row in inventory_data],
        "inventory": [float(row.quantity) for row in inventory_data],
        "consumption": [float(row.total_usage) for row in inventory_data],
        "restock": [float(row.total_restock) for row in inventory_data]
    }


    # Group usage by category for supply per service
    category_usage = {}
    for row in inventory_data:
        category_usage.setdefault(row.category, 0)
        category_usage[row.category] += float(row.total_usage)

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
