from flask import Blueprint, render_template, request
from app.models.branches import Branch, ClinicBranchImage
from app.models.employees import Employee
from app.models.patients import PatientsInfo
from app.models.patient_medical_info import PatientMedicalInfo
from app.models.procedures import Procedures
from app.models.transactions import Transactions

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
        patients = PatientsInfo.query.all()
    else:
        patients = PatientsInfo.query.filter_by(branch_id=selected_branch)
    
    branches = Branch.query.all()
    return render_template('/owner/patients.html', patients=patients, branches=branches, selected_branch=selected_branch)

@owner.route('/patient_info/<int:patient_id>')   
def patient_info(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    patient_medical_info = PatientMedicalInfo.query.get_or_404(patient_id)
    print(patient_medical_info.physician_name)
    return render_template('/owner/patient_info.html', patient=patient, patient_medical_info=patient_medical_info)

@owner.route('/patient_procedure/<int:patient_id>')   
def patient_procedure(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    procedures = Procedures.query.filter_by(patient_id=patient_id)
    return render_template('/owner/procedure.html',patient=patient, procedures=procedures)

@owner.route('/patient_dental_rec/<int:patient_id>')   
def patient_dental_rec(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    return render_template('/owner/dental_record.html', patient=patient)

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

@owner.route('/employee_work_details/<int:employee_id>')
def employee_work_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/em_work_details.html', employee=employee)

@owner.route('/employee_activity_details/<int:employee_id>')
def employee_activity_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/o_em_activity_details.html', employee=employee)

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
    transactions = Transactions.query.all()
    return render_template('/owner/transactions.html', transactions=transactions)

@owner.route('/balance_record')
def balance_record():
    # Get all procedures
    procedures = Procedures.query.all()
    balance_data = []

    for proc in procedures:
        total_fee = proc.fee
        payments = sum(t.total_amount_paid for t in proc.transactions)
        remaining = float(total_fee) - float(payments)

        if remaining > 0:  # Show only patients with balance
            balance_data.append({
                'patient': proc.patient,
                'last_visit': proc.procedure_date,
                'total_fee': total_fee,
                'amount_paid': payments,
                'remaining': remaining
            })

    return render_template('/owner/o_balance_rec.html', balance_data=balance_data)

@owner.route('/reports')    
def reports():
    return render_template('/owner/reports.html')