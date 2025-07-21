from flask import render_template, request, g
from app.models import InventoryItem, InventoryConsumable, InventoryEquipment

from app.views.dashboard import dashboard


@dashboard.route('/inventory')
def inventory():
    inventory_items = InventoryItem.query.all()
    return render_template('dashboard/inventory.html', inventory_items=inventory_items)

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

@dashboard.route('/inventory_lab_material')
def inventory_lab_material():
    return render_template('/dashboard/inventory_lab_materials.html')

@dashboard.route('/inventory_medication')
def inventory_medication():
    return render_template('/dashboard/inventory_medication.html')

@dashboard.route('/inventory_sterilization')
def inventory_sterilization():
    return render_template('/dashboard/inventory_sterilization.html')

@dashboard.before_app_request
def set_selected_branch():
    g.selected_branch = request.args.get('branch', 'all')

@dashboard.app_context_processor
def inject_selected_branch():
    return dict(selected_branch=g.get('selected_branch', 'all'))
