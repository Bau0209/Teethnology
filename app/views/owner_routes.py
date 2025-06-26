from flask import Blueprint, render_template

owner = Blueprint('owner', __name__)

@owner.route('/owner_home')
def owner_home():
    return render_template('/owner/O_home.html')

@owner.route('/branches')
def branches():
    return render_template('/owner/branches.html')

@owner.route('/branch_info')
def branch_info():
    return render_template('/owner/o_branch_info.html')

@owner.route('/appointments')
def appointments():
    return render_template('/owner/appointment.html')

@owner.route('/appointment_req')
def appointment_req():
    return render_template('/owner/appointment_req.html')

@owner.route('/patients')   
def patients():
    return render_template('/owner/patients.html')

@owner.route('/employees')
def employees():
    return render_template('/owner/employees.html')

@owner.route('/inventory')
def inventory():
    return render_template('/owner/inventory.html')

@owner.route('/transactions')
def transactions():
    return render_template('/owner/transactions.html')

@owner.route('/reports')    
def reports():
    return render_template('/owner/reports.html')