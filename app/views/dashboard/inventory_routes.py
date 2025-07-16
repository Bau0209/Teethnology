from flask import render_template

from app.views.dashboard import dashboard

@dashboard.route('/inventory')
def inventory():
    return render_template('/dashboard/inventory.html')

@dashboard.route('/inventory_equipment')
def inventory_equipment():
    return render_template('/dashboard/inventory_equipment.html')

@dashboard.route('/inventory_lab_material')
def inventory_lab_material():
    return render_template('/dashboard/inventory_lab_materials.html')

@dashboard.route('/inventory_medication')
def inventory_medication():
    return render_template('/dashboard/inventory_medication.html')

@dashboard.route('/inventory_sterilization')
def inventory_sterilization():
    return render_template('/dashboard/inventory_sterilization.html')
