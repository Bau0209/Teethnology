from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from app.models import Branch, PatientsInfo, PatientMedicalInfo, DentalInfo, Procedures, Transactions, Appointments, MainWeb
from app.utils.insights import generate_business_insight
from werkzeug.utils import secure_filename
import json
import os
from app import db
from datetime import datetime, date, timedelta

staff = Blueprint('staff', __name__)

#For image upload in branches
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import request
@staff.route('/staff_home')
# @role_required('staff')
def staff_home():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    selected_branch = request.args.get('branch', 'all')
    branches = Branch.query.all()
    main_web = MainWeb.query.first()

    if selected_branch == 'all':
        appointments_today = Appointments.query.filter(
            db.func.date(Appointments.appointment_sched) == today
        ).all()
        appointments_tomorrow = Appointments.query.filter(
            db.func.date(Appointments.appointment_sched) == tomorrow
        ).all()
        appointment_requests = Appointments.query.filter_by(appointment_status='pending').all()
    else:
        appointments_today = Appointments.query.filter(
            db.func.date(Appointments.appointment_sched) == today,
            Appointments.branch_id == int(selected_branch)
        ).all()
        appointments_tomorrow = Appointments.query.filter(
            db.func.date(Appointments.appointment_sched) == tomorrow,
            Appointments.branch_id == int(selected_branch)
        ).all()
        appointment_requests = Appointments.query.filter_by(
            branch_id=int(selected_branch),
            appointment_status='pending'
        ).all()

    insight_text = generate_business_insight()

    return render_template(
        '/staff/s_Home.html',
        appointments_today=appointments_today,
        appointments_tomorrow=appointments_tomorrow,
        appointment_requests=appointment_requests,
        branches=branches,
        selected_branch=selected_branch,
        main_web=main_web,
        insight_text=insight_text
    )

@staff.route('/appointments')
# @role_required('staff')
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
        'color': (
            "#228ad9" if a.procedures and a.procedures[0].procedure_status and 
            a.procedures[0].procedure_status.lower() == 'completed'
            else ('#e57373' if a.appointment_status == 'pending' else '#7bb3ad')
        ),
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
            'date': a.appointment_sched.strftime('%Y-%m-%d'),
            'procedure_status': (
                a.procedures[0].procedure_status.lower()
                if a.procedures and a.procedures[0].procedure_status
                else ''
            )
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

@staff.route('/appointment_req')
# @role_required('staff')
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

@staff.route('/appointments/<int:appointment_id>/status', methods=['POST'])
# @role_required('staff')
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

@staff.route('/patients')
# @role_required('v')
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
    
def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return None    

@staff.route('/patients/add', methods=['POST'])
def add_patient():    
    try:
        # Get patient_info fields
        branch_id = request.form.get('branch_id')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        birthdate = request.form.get('birthdate')
        sex = request.form.get('sex')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        address_line1 = request.form.get('address_line1')
        baranggay = request.form.get('baranggay')
        city = request.form.get('city')
        province = request.form.get('province')
        country = request.form.get('country')
        initial_consultation_reason = request.form.get('initial_consultation_reason')
        occupation = request.form.get('occupation')
        office_number = request.form.get('office_number')
        guardian_first_name = request.form.get('guardian_first_name')
        guardian_middle_name = request.form.get('guardian_middle_name')
        guardian_last_name = request.form.get('guardian_last_name')
        guardian_occupation = request.form.get('guardian_occupation')
        reffered_by = request.form.get('reffered_by')
        previous_dentist = request.form.get('previous_dentist')
        last_dentist_visit_raw = request.form.get('last_dentist_visit')
        last_dentist_visit = parse_date(last_dentist_visit_raw)

        # Create and save patient_info
        new_patient = PatientsInfo(
            branch_id=branch_id,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birthdate=birthdate,
            sex=sex,
            contact_number=contact_number,
            email=email,
            address_line1=address_line1,
            baranggay=baranggay,
            city=city,
            province=province,
            country=country,
            initial_consultation_reason=initial_consultation_reason,
            occupation=occupation,
            office_number=office_number,
            guardian_first_name=guardian_first_name,
            guardian_middle_name=guardian_middle_name,
            guardian_last_name=guardian_last_name,
            guardian_occupation=guardian_occupation,
            reffered_by=reffered_by,
            previous_dentist=previous_dentist,
            last_dental_visit=last_dentist_visit
        )
        db.session.add(new_patient)
        db.session.commit()  # needed to generate patient_id

        # Get patient_medical_info fields
        physician_name = request.form.get('physician_name')
        physician_specialty = request.form.get('physician_specialty')
        physician_office_address = request.form.get('physician_office_address')
        physician_office_number = request.form.get('physician_office_number')
        in_good_health = bool(request.form.get('in_good_health'))
        medical_treatment = request.form.get('medical_treatment_currently_undergoing')
        recent_illness = request.form.get('recent_illness_or_surgical_operation')
        when_illness = request.form.get('when_illness_or_operation')
        when_why_hospitalized = request.form.get('when_why_hospitalized')
        medications = request.form.get('medications_currently_taking')
        using_tabacco = bool(request.form.get('using_tabacco'))
        using_alcohol = bool(request.form.get('using_alcohol_cocaine_drugs'))
        allergies = request.form.get('allergies')
        bleeding_time = request.form.get('bleeding_time')
        is_pregnant = bool(request.form.get('is_pregnant'))
        is_nursing = bool(request.form.get('is_nursing'))
        on_birth_control = bool(request.form.get('on_birth_control'))
        blood_type = request.form.get('blood_type')
        blood_pressure = request.form.get('blood_pressure')
        illness_checklist = request.form.get('illness_checklist')

        # Create and save patient_medical_info
        medical_info = PatientMedicalInfo(
            patient_id=new_patient.patient_id,
            physician_name=physician_name,
            physician_specialty=physician_specialty,
            physician_office_address=physician_office_address,
            physician_office_number=physician_office_number,
            in_good_health=in_good_health,
            medical_treatment_currently_undergoing=medical_treatment,
            recent_illness_or_surgical_operation=recent_illness,
            when_illness_or_operation=when_illness,
            when_why_hospitalized=when_why_hospitalized,
            medications_currently_taking=medications,
            using_tabacco=using_tabacco,
            using_alcohol_cocaine_drugs=using_alcohol,
            allergies=allergies,
            bleeding_time=bleeding_time,
            is_pregnant=is_pregnant,
            is_nursing=is_nursing,
            on_birth_control=on_birth_control,
            blood_type=blood_type,
            blood_pressure=blood_pressure,
            illness_checklist=illness_checklist
        )
        db.session.add(medical_info)
        db.session.commit()
        
        # ---- Dental Info ----
        periodontal_screening = ','.join(request.form.getlist('periodontal_screening[]'))
        occlusion = ','.join(request.form.getlist('occlusion[]'))

        appliances = request.form.getlist('appliances[]')
        appliances_others = request.form.get('appliances_others')
        if appliances_others:
            appliances.append(appliances_others)
        appliances = ','.join(appliances)

        TMD = ','.join(request.form.getlist('TMD[]'))

        dental_info = DentalInfo(
            patient_id=new_patient.patient_id,
            dental_record_image_link="",  # You can replace this later with an uploaded image link
            periodontal_screening=periodontal_screening,
            occlusion=occlusion,
            appliances=appliances,
            TMD=TMD
        )

        db.session.add(dental_info)
        db.session.commit()

        flash("Patient record added successfully!", "success")
        return redirect(url_for('owner.patients'))
    
    except Exception as e:
        error_message = str(e)
        # Instead of redirecting, re-render the form with error
        return render_template(
            '/owner/patients.html',
            error_message=error_message,
            patients=[],  # or existing data if needed
            patient=None,
            patient_medical_info=None,
            dental_record=[],
            branches=Branch.query.all(),
            selected_branch='all'
        )
 
#Adding an Appointment in the calendar
@staff.route('/form', methods=['GET', 'POST'])
# @role_required('staff')
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

@staff.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
# @role_required('staff')
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

@staff.route('/patient_info/<int:patient_id>')   
# @role_required('staff')
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

@staff.route('/patient_procedure/<int:patient_id>') 
# @role_required('staff')  
def patient_procedure(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    procedures = Procedures.query.filter_by(patient_id=patient_id)
    return render_template('/owner/procedure.html',patient=patient, procedures=procedures)

@staff.route('/procedures/complete', methods=['POST'])
# @role_required('staff')
def complete_procedure():
    appointment_id = request.form.get('appointment_id')
    treatment_procedure = request.form.get('treatment_procedure')
    tooth_area = request.form.get('tooth_area')
    provider = request.form.get('provider')
    treatment_plan = request.form.get('treatment_plan')
    fee = int(float(request.form.get('fee')))
    payment_method = request.form.get('payment_method')
    total_paid = request.form.get('total_amount_paid')
    receipt_file = request.files.get('receipt')

    # Get appointment and patient
    appointment = Appointments.query.get(appointment_id)
    if not appointment:
        flash("Appointment not found.", "error")
        return redirect(url_for('owner.branches'))

    # Create procedure
    procedure = Procedures(
        patient_id=appointment.patient_id,
        appointment_id=appointment.appointment_id,
        procedure_date=date.today(),
        treatment_procedure=treatment_procedure,
        tooth_area=tooth_area,
        provider=provider,
        treatment_plan=treatment_plan,
        fee=fee,
        procedure_status='completed',
        notes='Recorded via modal'
    )
    db.session.add(procedure)
    db.session.commit()

    # Handle receipt upload
    receipt_path = None
    if receipt_file and receipt_file.filename:
        filename = secure_filename(receipt_file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/receipts')
        os.makedirs(upload_folder, exist_ok=True)
        receipt_path = os.path.join('static/uploads/receipts', filename)
        receipt_file.save(os.path.join(upload_folder, filename))

    # Create transaction
    transaction = Transactions(
        procedure_id=procedure.procedure_id,
        receipt_number=f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        payment_method=payment_method,
        transaction_datetime=datetime.now(),
        dentist_name=provider,
        service_detail=treatment_procedure,
        total_amount_paid=total_paid,
        transaction_image_link=receipt_path
    )
    db.session.add(transaction)
    db.session.commit()

    flash("Procedure and transaction successfully saved!", "success")
    return redirect(url_for('owner.appointments'))  # or wherever you list appointments

@staff.route('/patient_dental_rec/<int:patient_id>')   
# @role_required('staff')
def patient_dental_rec(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id)
    return render_template('/owner/dental_record.html', patient=patient, dental_record=dental_record)

@staff.route('/transactions')
# @role_required('staff')
def transactions():
    transactions = Transactions.query.all()
    return render_template('/owner/transactions.html', transactions=transactions)

@staff.route('/balance_record')
# @role_required('staff')
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
