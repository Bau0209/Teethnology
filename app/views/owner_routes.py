from flask import Blueprint, render_template, request
from app.models import Branch, ClinicBranchImage, Employee, PatientsInfo, PatientMedicalInfo, Procedures, Transactions, Appointments, DentalInfo
import json

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
    selected_branch = request.args.get('branch', 'all')
    appointment_id = request.args.get('appointment_id')

    query = Appointments.query

    if selected_branch != 'all':
        query = query.filter_by(branch_id=selected_branch)

    if appointment_id:
        query = query.filter_by(appointment_id=appointment_id)

    appointments = query.all()
    branches = Branch.query.all()

    events = [
        {
            'title': f"{a.patient.patient_full_name} - {a.appointment_type}",
            'start': a.appointment_sched.strftime('%Y-%m-%d')
        }
        for a in appointments
    ]
    
    appointment_data = [
        {
            'appointment_id': a.appointment_id,
            'status': a.appointment_status,
            'time': a.appointment_sched.strftime('%I:%M %p'),
            'reason': a.appointment_type,
            'patient_name': a.patient.patient_full_name,
            'patient_type': 'Returning Patient' if a.returning_patient else 'New Patient',
            'contact': a.patient.contact_number,
            'email': a.patient.email,
            'alternative_sched': a.alternative_sched.strftime('%Y-%m-%d %I:%M %p') if a.alternative_sched else None,
            'date': a.appointment_sched.strftime('%Y-%m-%d')
        }
        for a in appointments
    ]

    return render_template(
        '/owner/appointment.html',
        branches=branches,
        appointments=appointments,
        selected_branch=selected_branch,
        events=json.dumps(events),
        appointment_data=json.dumps(appointment_data)
    )

@owner.route('/appointment_req')
def appointment_req():
    selected_branch = request.args.get('branch', 'all')
    
    appointments = Appointments.query.filter_by(appointment_status='Pending')

    if selected_branch != 'all':
        appointments = appointments.filter_by(branch_id=selected_branch)

    appointment_data = [
        {
            'date': a.appointment_sched.strftime('%Y-%m-%d'),
            'time': a.appointment_sched.strftime('%I:%M %p'),
            'alternative_sched': a.alternative_sched.strftime('%Y-%m-%d %H:%M') if a.alternative_sched else None,
            'reason': a.appointment_type,
            'patient_name': a.patient.patient_full_name,
            'patient_type': 'Returning Patient' if a.returning_patient else 'New Patient',
            'dob': a.patient.birthdate.strftime('%Y-%m-%d'),
            'sex': a.patient.sex,
            'contact': a.patient.contact_number,
            'email': a.patient.email,
            'address': f"{a.patient.address_line1 + a.patient.baranggay + a.patient.city + a.patient.province + a.patient.country}"
        }
        for a in appointments
    ]
    
    branches = Branch.query.all()
    return render_template(
        '/owner/appointment_request.html',
        branches=branches,
        appointments=appointments,
        selected_branch=selected_branch,
        appointment_data=json.dumps(appointment_data)
    )

@owner.route('/appointment_req/<int:appointment_id>')
def appointment_req_detail(appointment_id):
    appointment = Appointments.query.get_or_404(appointment_id)

    appointment_data = {
        'date': appointment.appointment_sched.strftime('%Y-%m-%d'),
        'time': appointment.appointment_sched.strftime('%I:%M %p'),
        'alternative_sched': appointment.alternative_sched.strftime('%Y-%m-%d %H:%M') if appointment.alternative_sched else None,
        'reason': appointment.appointment_type,
        'patient_name': appointment.patient.patient_full_name,
        'patient_type': 'Returning Patient' if appointment.returning_patient else 'New Patient',
        'dob': appointment.patient.birthdate.strftime('%Y-%m-%d'),
        'sex': appointment.patient.sex,
        'contact': appointment.patient.contact_number,
        'email': appointment.patient.email,
        'address': f"{appointment.patient.address_line1 + appointment.patient.baranggay + appointment.patient.city + appointment.patient.province + appointment.patient.country}"
    }

    return render_template(
        '/owner/appointment_request.html',
        appointment=appointment,
        appointment_data=appointment_data
    )


@owner.route('/patients')
def patients():
    selected_branch = request.args.get('branch', 'all')
    
    if selected_branch == 'all':
        patients = PatientsInfo.query.all()
    else:
        patients = PatientsInfo.query.filter_by(branch_id=selected_branch).all()
    
    branches = Branch.query.all()
    return render_template(
        '/owner/patients.html',
        patients=patients,
        branches=branches,
        selected_branch=selected_branch
    )

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
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id)
    return render_template('/owner/dental_record.html', patient=patient, dental_record=dental_record)

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

@owner.route('/report_patients')    
def report_patients():
    return render_template('/owner/o_rep_patient.html')

@owner.route('/report_marketing')    
def report_marketing():
    return render_template('/owner/o_rep_marketing.html')

@owner.route('/report_inventory')    
def report_inventory():
    return render_template('/owner/o_rep_inventory.html')