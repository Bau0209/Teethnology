from flask import render_template, request, g
from app.models import InventoryItem, InventoryConsumable,InventoryMedication, InventoryLabMaterial, InventoryEquipment, InventorySterilization

from app.views.dashboard import dashboard

@dashboard.before_app_request
def set_selected_branch():
    g.selected_branch = request.args.get('branch', 'all')

@dashboard.app_context_processor
def inject_selected_branch():
    return dict(selected_branch=g.get('selected_branch', 'all'))

@dashboard.route('/inventory')
def inventory():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('dashboard/inventory.html', inventory_items=items)

@dashboard.route('/inventory_consumable')
def inventory_consumable():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query.join(InventoryConsumable)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('dashboard/inventory_consumable.html', inventory_items=items)

@dashboard.route('/inventory_equipment')
def inventory_equipment():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query.join(InventoryEquipment)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('dashboard/inventory_equipment.html', inventory_items=items)

@dashboard.route('/inventory_sterilization')
def inventory_sterilization():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query.join(InventorySterilization)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('/dashboard/inventory_sterilization.html', inventory_items=items)

@dashboard.route('/inventory_lab_material')
def inventory_lab_material():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query.join(InventoryLabMaterial)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('/dashboard/inventory_lab_material.html', inventory_items=items)

@dashboard.route('/inventory_medication')
def inventory_medication():
    selected_branch = g.get('selected_branch', 'all')
    query = InventoryItem.query.join(InventoryMedication)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.all()
    return render_template('/dashboard/inventory_medication.html', inventory_items=items)


