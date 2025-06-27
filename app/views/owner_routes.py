from flask import Blueprint, render_template
from app.models.branches import Branch, ClinicBranchImage

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
    return render_template('/owner/patients.html')

@owner.route('/patient_info')   
def patient_info():
    return render_template('/owner/patient_info.html')

@owner.route('/patient_procedure')   
def patient_procedure():
    return render_template('/owner/procedure.html')

@owner.route('/patient_dental_rec')   
def patient_dental_rec():
    return render_template('/owner/dental_record.html')

@owner.route('/employees')
def employees():
    return render_template('/owner/employees.html')

@owner.route('/employee_info')
def employee_info():
    return render_template('/owner/employee_basic_info.html')

@owner.route('/inventory')
def inventory():
    return render_template('/owner/inventory.html')

@owner.route('/transactions')
def transactions():
    return render_template('/owner/transactions.html')

@owner.route('/reports')    
def reports():
    return render_template('/owner/reports.html')