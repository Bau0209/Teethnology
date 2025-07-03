from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from app.models import Branch, ClinicBranchImage, Employee, PatientsInfo, PatientMedicalInfo, DentalInfo, Procedures, Transactions, Appointments, MainWeb
from werkzeug.utils import secure_filename
from .auth import role_required
import json
import os
from app import db
from datetime import datetime

owner = Blueprint('owner', __name__)

#For image upload in branches
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@owner.route('/owner_home')
# @role_required('owner')
def owner_home():
    return render_template('/owner/O_home.html')

@owner.route('/branches')
# @role_required('owner')
def branches():
    main_web = MainWeb.query.first()
    branches = Branch.query.all()

    # For each branch, get its first image (if any)
    branch_images = {}
    for branch in branches:
        first_image = ClinicBranchImage.query.filter_by(branch_id=branch.branch_id).first()
        branch_images[branch.branch_id] = first_image.image_link if first_image else None

    return render_template(
        '/owner/branches.html',
        branches=branches,
        main_web=main_web,
        branch_images=branch_images
    )

@owner.route('/branch_info/<int:branch_id>')
# @role_required('owner')
def branch_info(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/owner/o_branch_info.html', branch=branch, branch_images=branch_images)

@owner.route('/update-main-website', methods=['POST'])
# @role_required('owner')
def update_main_website():
    main_web = MainWeb.query.first()
    if not main_web:
        main_web = MainWeb()

    # Get values from form
    services = request.form.getlist('services')
    main_web.services = ','.join(services)
    main_web.about_us = request.form.get('about_us')
    main_web.main_email = request.form.get('main_email')
    main_web.main_contact_number = request.form.get('main_contact_number')

    # Save to DB
    db.session.add(main_web)
    db.session.commit()
    flash('Website info updated successfully.', 'success')
    return redirect(url_for('owner.branches'))

@owner.route('/branch/<int:branch_id>/add-image', methods=['POST'])
# @role_required('owner')
def add_branch_image(branch_id):
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.referrer)

    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Save to DB
        rel_path = os.path.relpath(filepath, 'static').replace('\\', '/')

        new_image = ClinicBranchImage(
            image_link=rel_path,
            branch_id=branch_id
        )

        db.session.add(new_image)
        db.session.commit()
        flash('Image uploaded successfully.')
    else:
        flash('Invalid file type.')

    return redirect(request.referrer)

@owner.route('/branch/<int:image_id>/delete-image', methods=['POST'])
# @role_required('owner')
def delete_branch_image(image_id):
    image = ClinicBranchImage.query.get(image_id)
    if image:
        filepath = os.path.join('static', image.image_link)
        if os.path.exists(filepath):
            os.remove(filepath)

        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully.')
    else:
        flash('Image not found.')

    return redirect(request.referrer)

@owner.route('/branch/<int:branch_id>/edit', methods=['POST'])
# @role_required('owner')
def edit_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)

    branch.branch_name = request.form['branch_name']
    branch.full_address = request.form['full_address']
    branch.services = request.form['services']
    branch.clinic_description = request.form['clinic_description']
    branch.chief_dentist = request.form['chief_dentist']
    branch.contact_number = request.form['contact_number']
    branch.clinic_open_hour = request.form['clinic_open_hour']
    branch.clinic_close_hour = request.form['clinic_close_hour']

    db.session.commit()
    flash('Branch information updated successfully.', 'success')
    return redirect(url_for('owner.branch_info', branch_id=branch_id))

@owner.route('/appointments')
# @role_required('owner')
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
        'start': a.appointment_sched.strftime('%Y-%m-%d'),
        'color': '#e57373' if a.appointment_status == 'pending' else '#7bb3ad',
        'patient': a.patient.patient_full_name,
        'type': a.appointment_type,
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
# @role_required('owner')
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

@owner.route('/appointments/<int:appointment_id>/status', methods=['POST'])
# @role_required('owner')
def update_appointment_status(appointment_id):
    data = request.get_json()
    status = data.get('status')

    if status not in ['approved', 'cancelled', 'completed']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400

    appointment = Appointments.query.get(appointment_id)
    if not appointment:
        return jsonify({'success': False, 'message': 'Appointment not found'}), 404

    # Update appointment status
    appointment.appointment_status = status

    # Also update procedure_status if it's 'completed' or 'cancelled'
    if status in ['completed', 'cancelled']:
        procedures = Procedures.query.filter_by(appointment_id=appointment_id).all()
        if not procedures:
            return jsonify({'success': False, 'message': 'No procedure records found for this appointment'}), 404

        for proc in procedures:
            proc.procedure_status = status

    db.session.commit()

    return jsonify({'success': True, 'message': 'Status updated successfully'})

@owner.route('/patients')
# @role_required('owner')
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
        patient=None,
        patient_medical_info=None,
        dental_record=[],
        branches=branches,
        selected_branch=selected_branch
    )

#Adding an Appointment in the calendar
@owner.route('/form', methods=['GET', 'POST'])
# @role_required('owner')
def form():
    branches = Branch.query.all()
    if request.method == 'POST':
        is_returning = request.form.get('firstvisit') == 'yes'
        first_name = request.form.get('first_name', '').strip().lower()
        last_name = request.form.get('last_name', '').strip().lower()
        branch_id = int(request.form.get('branch_id'))
        # Convert 'male'/'female' to 'M'/'F'
        raw_gender = request.form.get('sex', '').lower()
        sex = 'M' if raw_gender == 'male' else 'F' if raw_gender == 'female' else None

        if is_returning:
            # Validate returning patient by ID and name
            patient_id = int(request.form.get('patient_id'))
            patient = PatientsInfo.query.filter_by(patient_id=patient_id).first()
            if not patient or patient.first_name.lower() != first_name or patient.last_name.lower() != last_name:
                flash(f"Invalid Patient ID or Name. Please try again.", "danger")
                flash(f"Entered ID: {patient_id}", "danger")
                flash(f"Entered Name: {first_name.title()} {last_name.title()}", "danger")

                if patient:
                    flash(f"DB Name: {patient.first_name.title()} {patient.last_name.title()}", "danger")
                else:
                    flash("No patient found with that ID.", "danger")

                return redirect(request.referrer)

            # Create appointment
            new_appointment = Appointments(
                branch_id=branch_id,
                patient_id=patient.patient_id,
                appointment_sched=datetime.fromisoformat(request.form.get('preferred')),
                alternative_sched=datetime.fromisoformat(request.form.get('alternative')) if request.form.get('alternative') else None,
                appointment_type=request.form.get('appointment_type'),
                appointment_status='pending',
                returning_patient=True
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment booked successfully for returning patient.", "success")
            return redirect(url_for('owner.appointments'))

        else:
            # Register new patient
            new_patient = PatientsInfo(
                branch_id=branch_id,
                first_name=request.form.get('first_name'),
                middle_name=request.form.get('middle_name'),
                last_name=request.form.get('last_name'),
                birthdate=request.form.get('dob'),
                sex=sex,
                contact_number=request.form.get('contact'),
                email=request.form.get('email'),
                address_line1=request.form.get('address_line1'),
                baranggay=request.form.get('baranggay'),
                city=request.form.get('city'),
                province=request.form.get('province'),
                country=request.form.get('country'),
                initial_consultation_reason=request.form.get('appointment_type')
            )
            db.session.add(new_patient)
            db.session.commit()

            # Create appointment
            new_appointment = Appointments(
                branch_id=branch_id,
                patient_id=new_patient.patient_id,
                appointment_sched=datetime.fromisoformat(request.form.get('preferred')),
                alternative_sched=datetime.fromisoformat(request.form.get('alternative')) if request.form.get('alternative') else None,
                appointment_type=request.form.get('appointment_type'),
                appointment_status='pending',
                returning_patient=False
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment booked successfully for new patient.", "success")
            return redirect(url_for('owner.appointments'))

    return render_template('/owner/appointment.html', branches=branches)

@owner.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
# @role_required('owner')
def edit_patient(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    patient_medical_info = PatientMedicalInfo.query.get(patient_id)
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id).all() or []

    form_type = request.args.get("form") 
    
    if request.method == 'POST':
        form_type = request.args.get("form") or request.form.get("form")
        if form_type =="patient_info":
            try:
                # -------- Patient Info Update --------
                patient.first_name = request.form.get('first_name')
                patient.middle_name = request.form.get('middle_name')
                patient.last_name = request.form.get('last_name')
                patient.birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d')
                patient.sex = request.form.get('sex')
                patient.contact_number = request.form.get('contact_number')
                patient.email = request.form.get('email')
                patient.address_line1 = request.form.get('address_line1')
                patient.baranggay = request.form.get('baranggay')
                patient.city = request.form.get('city')
                patient.province = request.form.get('province')
                patient.country = request.form.get('country')
                patient.initial_consultation_reason = request.form.get('initial_consultation_reason')
                patient.occupation = request.form.get('occupation')
                patient.office_number = request.form.get('office_number')
                patient.guardian_first_name = request.form.get('guardian_first_name')
                patient.guardian_middle_name = request.form.get('guardian_middle_name')
                patient.guardian_last_name = request.form.get('guardian_last_name')
                patient.guardian_occupation = request.form.get('guardian_occupation')
                patient.reffered_by = request.form.get('reffered_by')
                patient.previous_dentist = request.form.get('previous_dentist')
                last_visit = request.form.get('last_dental_visit')
                patient.last_dental_visit = datetime.strptime(last_visit, '%Y-%m-%d') if last_visit else None

                # -------- Medical Info Update --------
                if patient_medical_info:
                    patient_medical_info.physician_name = request.form.get('physician_name')
                    patient_medical_info.physician_specialty = request.form.get('physician_specialty')
                    patient_medical_info.physician_office_address = request.form.get('physician_office_address')
                    patient_medical_info.physician_office_number = request.form.get('physician_office_number')
                    patient_medical_info.in_good_health = bool(request.form.get('in_good_health'))
                    patient_medical_info.medical_treatment_currently_undergoing = request.form.get('medical_treatment_currently_undergoing')
                    patient_medical_info.recent_illness_or_surgical_operation = request.form.get('recent_illness_or_surgical_operation')
                    patient_medical_info.when_illness_or_operation = request.form.get('when_illness_or_operation')
                    patient_medical_info.when_why_hospitalized = request.form.get('when_why_hospitalized')
                    patient_medical_info.medications_currently_taking = request.form.get('medications_currently_taking')
                    patient_medical_info.using_tabacco = bool(request.form.get('using_tabacco'))
                    patient_medical_info.using_alcohol_cocaine_drugs = bool(request.form.get('using_alcohol_cocaine_drugs'))
                    patient_medical_info.allergies = ','.join(request.form.getlist('allergy'))
                    patient_medical_info.bleeding_time = request.form.get('bleeding_time')
                    patient_medical_info.is_pregnant = bool(request.form.get('is_pregnant'))
                    patient_medical_info.is_nursing = bool(request.form.get('is_nursing'))
                    patient_medical_info.on_birth_control = bool(request.form.get('on_birth_control'))
                    patient_medical_info.blood_type = request.form.get('blood_type')
                    patient_medical_info.blood_pressure = request.form.get('blood_pressure')
                    patient_medical_info.illness_checklist = ','.join(request.form.getlist('illness_checklist'))

                db.session.commit()
                flash("Patient record updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash("Error updating patient record: " + str(e), "danger")
        elif form_type == "dental_record":
            try:
                # Clear old records (optional — depends if you want to replace them)
                DentalInfo.query.filter_by(patient_id=patient_id).delete()

                # Get form data
                periodontal = request.form.getlist('periodontal_screening')
                occlusion = request.form.getlist('occlusion')
                appliances = request.form.getlist('appliances')
                tmd = request.form.getlist('TMD')
                image_link = request.form.get('dental_record_image_link') or "default.png"  # fallback

                new_record = DentalInfo(
                    patient_id=patient_id,
                    periodontal_screening=','.join(periodontal),
                    occlusion=','.join(occlusion),
                    appliances=','.join(appliances),
                    TMD=','.join(tmd),
                    dental_record_image_link=image_link
                )

                db.session.add(new_record)
                db.session.commit()
                flash("Dental record updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash("Error updating dental record: " + str(e), "danger")
            
            return redirect(url_for('owner.edit_patient', patient_id=patient_id))

    # GET request
    return render_template(
        'owner/patient_info.html',
        patient=patient,
        dental_record=dental_record,
        patient_medical_info=patient_medical_info,
        current_date=datetime.today().date()
    )

@owner.route('/patient_info/<int:patient_id>')   
# @role_required('owner')
def patient_info(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)  # Required
    patient_medical_info = PatientMedicalInfo.query.get(patient_id)  # Optional
    dental_info = DentalInfo.query.get(patient_id)  # Optional (if you're including dental info too)

    return render_template(
        '/owner/patient_info.html',
        patient=patient,
        patient_medical_info=patient_medical_info,
        dental_info=dental_info
    )

@owner.route('/patient_procedure/<int:patient_id>') 
# @role_required('owner')  
def patient_procedure(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    procedures = Procedures.query.filter_by(patient_id=patient_id)
    return render_template('/owner/procedure.html',patient=patient, procedures=procedures)

@owner.route('/procedures/<int:appointment_id>/status', methods=['POST'])
# @role_required('owner')
def update_procedure_status(appointment_id):
    data = request.get_json()
    status = data.get('status')

    if status not in ['completed', 'cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400

    # Find procedures with the given appointment_id
    procedures = Procedures.query.filter_by(appointment_id=appointment_id).all()

    if not procedures:
        return jsonify({
            'success': False,
            'message': f'No procedure found for this appointment (ID: {appointment_id}). Please add the procedure to this patient\'s history first.'
        }), 404

    # Update all matching procedures (in case there's more than one)
    for procedure in procedures:
        procedure.procedure_status = status

    db.session.commit()

    return jsonify({'success': True, 'message': 'Procedure status updated.'})

@owner.route('/patient_dental_rec/<int:patient_id>')   
# @role_required('owner')
def patient_dental_rec(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id)
    return render_template('/owner/dental_record.html', patient=patient, dental_record=dental_record)

@owner.route('/employees')
# @role_required('owner')
def employees():
    selected_branch = request.args.get('branch', 'all')
    
    if selected_branch == 'all':
        employees = Employee.query.all()
    else:
        employees = Employee.query.filter_by(branch_id=selected_branch)
    
    branches = Branch.query.all()
    return render_template('/owner/employees.html', branches=branches, employees=employees)

@owner.route('/employee_info/<int:employee_id>')
# @role_required('owner')
def employee_info(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/employee_basic_info.html', employee=employee)

@owner.route('/employee_work_details/<int:employee_id>')
# @role_required('owner')
def employee_work_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/em_work_details.html', employee=employee)

@owner.route('/employee_activity_details/<int:employee_id>')
# @role_required('owner')
def employee_activity_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/o_em_activity_details.html', employee=employee)

@owner.route('/inventory')
# @role_required('owner')
def inventory():
    return render_template('/owner/inventory.html')

@owner.route('/inventory_equipment')
# @role_required('owner')
def inventory_equipment():
    return render_template('/owner/o_in_equipment.html')

@owner.route('/inventory_lab_material')
# @role_required('owner')
def inventory_lab_material():
    return render_template('/owner/o_in_lab_materials.html')

@owner.route('/inventory_medication')
# @role_required('owner')
def inventory_medication():
    return render_template('/owner/o_in_medication.html')

@owner.route('/inventory_sterilization')
# @role_required('owner')
def inventory_sterilization():
    return render_template('/owner/o_in_sterilization.html')

@owner.route('/transactions')
# @role_required('owner')
def transactions():
    transactions = Transactions.query.all()
    return render_template('/owner/transactions.html', transactions=transactions)

@owner.route('/balance_record')
# @role_required('owner')
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
# @role_required('owner')
def reports():
    return render_template('/owner/reports.html')

@owner.route('/report_patients') 
# @role_required('owner')   
def report_patients():
    return render_template('/owner/o_rep_patient.html')

@owner.route('/report_marketing')    
# @role_required('owner')
def report_marketing():
    return render_template('/owner/o_rep_marketing.html')

@owner.route('/report_inventory') 
# @role_required('owner')   
def report_inventory():
    return render_template('/owner/o_rep_inventory.html')

