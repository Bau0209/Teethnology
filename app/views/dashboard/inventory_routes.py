from flask import render_template, request, g
from app.models import InventoryItem, InventoryConsumable,InventoryMedication, InventoryLabMaterial, InventoryEquipment, InventorySterilization

from app.views.dashboard import dashboard

@dashboard.before_app_request
def set_selected_branch():
    g.selected_branch = request.args.get('branch', 'all')

@dashboard.app_context_processor
def inject_selected_branch():
    return dict(selected_branch=g.get('selected_branch', 'all'))

from sqlalchemy.orm import joinedload

@dashboard.route('/inventory')
def inventory():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = InventoryItem.query.options(
        joinedload(InventoryItem.equipment_info),
        joinedload(InventoryItem.consumable_info),
        joinedload(InventoryItem.sterilization_info),
        joinedload(InventoryItem.medication_info),
        joinedload(InventoryItem.lab_material_info),
    )

    if selected_branch != 'all':
        query = query.filter_by(branch_id=selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'dashboard/inventory.html',
        inventory_items=items.items,
        pagination=items
    )

    
@dashboard.route('/inventory_consumable')
def inventory_consumable():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = InventoryItem.query.join(InventoryConsumable)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'dashboard/inventory_consumable.html', 
        inventory_items=items,
        pagination=items
    )

@dashboard.route('/inventory_equipment')
def inventory_equipment():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = InventoryItem.query.join(InventoryEquipment)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'dashboard/inventory_equipment.html', 
        inventory_items=items,
        pagination=items
    )

@dashboard.route('/inventory_sterilization')
def inventory_sterilization():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = InventoryItem.query.join(InventorySterilization)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'dashboard/inventory_sterilization.html', 
        inventory_items=items,
        pagination=items
    )

@dashboard.route('/inventory_lab_material')
def inventory_lab_material():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = InventoryItem.query.join(InventoryLabMaterial)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        '/dashboard/inventory_lab_material.html',
        inventory_items=items,
        pagination=items
    )

@dashboard.route('/inventory_medication')
def inventory_medication():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = InventoryItem.query.join(InventoryMedication)

    if selected_branch != 'all':
        query = query.filter(InventoryItem.branch_id == selected_branch)

    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        '/dashboard/inventory_medication.html', 
        inventory_items=items,
        pagination=items
    )


