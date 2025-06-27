from flask import Blueprint, render_template, request
from app.models.branches import Branch, ClinicBranchImage
from app.models.employees import Employee
from app.models.patients import Patients

owner = Blueprint('owner', __name__)

@owner.route('/owner_home')
def owner_home():
    return render_template('/owner/O_home.html')

@owner.route('/branches')
def branches():
    branches = Branch.query.all()
    return render_template('/owner/branches.html', branches=branches)

@owner.route('/branch_info/<int:branch_id>')
def branch_info(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/owner/o_branch_info.html', branch=branch, branch_images=branch_images)

@owner.route('/appointments')
def appointments():
    return render_template('/owner/appointment.html')

@owner.route('/appointment_req')
def appointment_req():
    return render_template('/owner/appointment_request.html')

@owner.route('/patients')   
def patients():
    selected_branch = request.args.get('branch', 'all')
    
    if selected_branch == 'all':
        patients = Patients.query.all()
    else:
        patients = Patients.query.filter_by(branch_id=selected_branch)
    
    branches = Branch.query.all()
    return render_template('/owner/patients.html', patients=patients, branches=branches, selected_branch=selected_branch)

@owner.route('/patient_info/<int:patient_id>')   
def patient_info(patient_id):
    patient = Patients.query.get_or_404(patient_id)
    return render_template('/owner/patient_info.html', patient=patient)

@owner.route('/patient_procedure')   
def patient_procedure():
    return render_template('/owner/procedure.html')

@owner.route('/patient_dental_rec')   
def patient_dental_rec():
    return render_template('/owner/dental_record.html')

@owner.route('/employees')
def employees():
    selected_branch = request.args.get('branch', 'all')
    
    if selected_branch == 'all':
        employees = Employee.query.all()
    else:
        employees = Employee.query.filter_by(branch_id=selected_branch)
    
    branches = Branch.query.all()
    return render_template('/owner/employees.html', branches=branches, employees=employees)

@owner.route('/employee_info/<int:employee_id>')
def employee_info(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/employee_basic_info.html', employee=employee)

@owner.route('/inventory')
def inventory():
    return render_template('/owner/inventory.html')

@owner.route('/inventory_equipment')
def inventory_equipment():
    return render_template('/owner/o_in_equipment.html')

@owner.route('/inventory_lab_material')
def inventory_lab_material():
    return render_template('/owner/o_in_lab_materials.html')

@owner.route('/inventory_medication')
def inventory_medication():
    return render_template('/owner/o_in_medication.html')

@owner.route('/inventory_sterilization')
def inventory_sterilization():
    return render_template('/owner/o_in_sterilization.html')

@owner.route('/transactions')
def transactions():
    return render_template('/owner/transactions.html')

@owner.route('/reports')    
def reports():
    return render_template('/owner/reports.html')