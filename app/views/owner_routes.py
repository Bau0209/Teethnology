from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from app.models import Account, Branch, ClinicBranchImage, Employee, PatientsInfo, PatientMedicalInfo, DentalInfo, Procedures, Transactions, Appointments, MainWeb
from app.utils.insights import generate_business_insight
from werkzeug.utils import secure_filename
from .auth import role_required
import json
import os
from app import db
from datetime import datetime, date, timedelta
from sqlalchemy import extract, func
from collections import defaultdict

owner = Blueprint('owner', __name__)

#For image upload in branches
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@owner.route('/owner_home')
def owner_home():
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
        appointment_requests = Appointments.query.filter_by(
            appointment_status='pending'
        ).order_by(Appointments.appointment_sched.asc()).all()

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
        ).order_by(Appointments.appointment_sched.asc()).all()

    insight_text = generate_business_insight()

    return render_template(
        '/owner/O_home.html',
        appointments_today=appointments_today,
        appointments_tomorrow=appointments_tomorrow,
        appointment_requests=appointment_requests,
        branches=branches,
        selected_branch=selected_branch,
        main_web=main_web,
        insight_text=insight_text
    )

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

@owner.route('/branches/add', methods=['POST'])
# @role_required('owner')
def add_branch():    
    branch_name = request.form.get('branch_name')
    full_address = request.form.get('full_address')
    description = request.form.get('description')
    chief_dentist = request.form.get('chief_dentist')
    contact_number = request.form.get('contact')
    open_time = request.form.get('open_time')
    close_time = request.form.get('close_time')
    services_list = request.form.getlist('services[]')
    services = ', '.join(services_list)

    # Check if branch name already exists
    if Branch.query.filter_by(branch_name=branch_name).first():
        flash('Branch name already exists.', 'error')
        return redirect(url_for('owner.branches'))

    # Convert times
    open_hour = datetime.strptime(open_time, '%H:%M').time()
    close_hour = datetime.strptime(close_time, '%H:%M').time()

    # Handle image upload
    image_file = request.files.get('image')
    if not image_file:
        flash('Image is required.', 'error')
        return redirect(url_for('owner.branches'))

    filename = secure_filename(image_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    # Save image to filesystem
    image_path = os.path.join(upload_folder, filename)
    image_file.save(image_path)

    # Save branch to DB
    new_branch = Branch(
        branch_name=branch_name,
        full_address=full_address,
        clinic_description=description,
        chief_dentist=chief_dentist,
        contact_number=contact_number,
        clinic_open_hour=open_hour,
        clinic_close_hour=close_hour,
        services=services
    )
    db.session.add(new_branch)
    db.session.commit()

    # Save image path to DB (relative to static/)
    image_link = f"uploads/branches/{filename}"  # ✅ relative URL path
    new_image = ClinicBranchImage(
        image_link=image_link,
        branch_id=new_branch.branch_id
    )
    db.session.add(new_image)
    db.session.commit()

    flash('Branch successfully added!', 'success')
    return redirect(url_for('owner.branches'))

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
    return redirect(url_for('owner.owner_home'))

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
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'branches')
        
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

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return None    

@owner.route('/patients/add', methods=['POST'])
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

# @owner.route('/procedures/<int:appointment_id>/status', methods=['POST'])
# # @role_required('owner')
# def update_procedure_status(appointment_id):
#     data = request.get_json()
#     status = data.get('status')

#     if status not in ['completed', 'cancelled']:
#         return jsonify({'success': False, 'message': 'Invalid status'}), 400

#     procedures = Procedures.query.filter_by(appointment_id=appointment_id).all()

#     if not procedures:
#         # Get appointment info to seed procedure
#         appointment = Appointments.query.get(appointment_id)
#         if not appointment:
#             return jsonify({'success': False, 'message': 'Appointment not found.'}), 404

#         # Create new Procedure using data from appointment
#         new_procedure = Procedures(
#             patient_id=appointment.patient_id,
#             appointment_id=appointment_id,
#             procedure_date=date.today(),
#             treatment_procedure="General Treatment",  # default or replace later
#             tooth_area="N/A",
#             provider=appointment.approved_by or "Unknown",
#             treatment_plan="Auto-generated on status update.",
#             fee=0,  # default or override later
#             procedure_status=status,
#             notes="Procedure created via status update."
#         )
#         db.session.add(new_procedure)
#         db.session.commit()

#         # Create matching transaction (optional defaults)
#         new_transaction = Transactions(
#             procedure_id=new_procedure.procedure_id,
#             receipt_number=f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             payment_method="Other",  # or "Cash", if you want
#             transaction_datetime=datetime.now(),
#             dentist_name=new_procedure.provider,
#             service_detail=new_procedure.treatment_procedure,
#             total_amount_paid=0.00,  # set real value later
#             transaction_image_link=None
#         )
#         db.session.add(new_transaction)
#         db.session.commit()

#         return jsonify({'success': True, 'message': 'Procedure and transaction created and marked as ' + status + '.'})

#     # If procedure(s) already exist, just update all their statuses
#     for procedure in procedures:
#         procedure.procedure_status = status

#     db.session.commit()

#     return jsonify({'success': True, 'message': 'Procedure status updated.'})

@owner.route('/procedures/complete', methods=['POST'])
# @role_required('owner')
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

@owner.route('/patient_dental_rec/<int:patient_id>')   
# @role_required('owner')
def patient_dental_rec(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id)
    return render_template('/owner/dental_record.html', patient=patient, dental_record=dental_record)

@owner.route('/employees', methods=['GET', 'POST'])
# @role_required('owner')
def employees():
    selected_branch = request.args.get('branch', 'all')
    branches = Branch.query.all()

    # --- Handle form submission ---
    if request.method == 'POST':
        # Get form data
        branch_id = request.form.get('branch_id')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        sex = request.form.get('sex')
        birthdate = request.form.get('birthdate')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        date_hired = request.form.get('date_hired')
        position = request.form.get('position')
        department = request.form.get('department')
        shift_days = request.form.get('shift_days')
        shift_hours = request.form.get('shift_hours')

        # Create new employee object
        new_employee = Employee(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            sex=sex,
            birthdate=birthdate,
            contact_number=contact_number,
            email=email,
            employment_status='active',  # default
            date_hired=date_hired,
            position=position,
            department=department,
            shift_days=shift_days,
            shift_hours=shift_hours,
            branch_id=branch_id
        )

        # Add to database
        db.session.add(new_employee)
        db.session.commit()
        flash('New employee added successfully!', 'success')
        return redirect(url_for('owner.employees', branch=selected_branch))

    # --- Handle GET: fetch employees based on selected branch ---
    if selected_branch == 'all':
        employees = Employee.query.all()
    else:
        employees = Employee.query.filter_by(branch_id=selected_branch).all()

    return render_template('/owner/employees.html', 
                           branches=branches, 
                           selected_branch=selected_branch,
                           employees=employees, 
                           employee=None,
                           today=date.today())

@owner.route('/edit_employee/<int:employee_id>', methods=['POST'])
# @role_required('owner')
def edit_employee(employee_id):
    form_type = request.args.get("form")
    
    if form_type == "basic_info":
        employee = Employee.query.get_or_404(employee_id)
        birthdate_str = request.form.get('birthdate')  # e.g., '2025-08-02'
        date_hired_str = request.form.get('date_hired')
        
        try:
            employee.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            employee.date_hired = datetime.strptime(date_hired_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(request.referrer)

        # Other fields
        employee.first_name = request.form.get('first_name')
        employee.middle_name = request.form.get('middle_name')
        employee.last_name = request.form.get('last_name')
        employee.sex = request.form.get('sex')
        employee.employment_status = request.form.get('employment_status')
        employee.contact_number = request.form.get('contact_number')
        employee.email = request.form.get('email')
        
        db.session.commit()
        flash("Employee updated successfully!", "success")
        return redirect(url_for('owner.employee_info', employee_id=employee_id))
    elif form_type == "work_details":
        employee = Employee.query.get_or_404(employee_id)
        account = Account.query.filter_by(employee_id=employee_id).first()

        # Update Employee fields
        employee.position = request.form.get('position')
        employee.department = request.form.get('department')
        employee.shift_days = request.form.get('shift_days')
        employee.shift_hours = request.form.get('shift_hours')

        # Optional: If position is duplicated in Account, also update account
        if account:
            account.position = request.form.get('position')  # Only if Account has this field

        db.session.commit()
        flash("Work details updated successfully!", "success")
        return redirect(url_for('owner.employee_work_details', employee_id=employee_id))
    

@owner.route('/employee_info/<int:employee_id>')
# @role_required('owner')
def employee_info(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/employee_basic_info.html', employee=employee)

@owner.route('/employee_work_details/<int:employee_id>')
# @role_required('owner')
def employee_work_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)    
    account = Account.query.filter_by(employee_id=employee_id).first()
    return render_template('/owner/em_work_details.html', employee=employee, account=account)

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

@owner.route('/reports_copy')
# @role_required('owner')
def reports_copy():
    
    return render_template('owner/reports_copy.html')

@owner.route('/reports')    
# @role_required('owner')
def reports():
    # Get current and last month
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    selected_year = request.args.get('year', type=int) or current_year
    last_month = current_month - 1 if current_month > 1 else 12
    
    # Today's Revenue
    today = date.today()
    today_revenue = db.session.query(
        func.sum(Transactions.total_amount_paid)
    ).filter(
        func.date(Transactions.transaction_datetime) == today
    ).scalar() or 0

    # Revenue per month (for chart)
    revenue_data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        func.sum(Transactions.total_amount_paid).label('total')
    ).filter(
        extract('year', Transactions.transaction_datetime) == selected_year
    ).group_by(
        extract('month', Transactions.transaction_datetime)
    ).order_by(
        extract('month', Transactions.transaction_datetime)
    ).all()
    
    unchangable_revenue_data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        func.sum(Transactions.total_amount_paid).label('total')
    ).filter(
        extract('year', Transactions.transaction_datetime) == current_year
    ).group_by(
        extract('month', Transactions.transaction_datetime)
    ).order_by(
        extract('month', Transactions.transaction_datetime)
    ).all()

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    values = [0] * 12

    for month, total in unchangable_revenue_data:
        values[int(month) - 1] = float(total)

    # Current month revenue
    current_revenue = values[current_month - 1]
    last_revenue = values[last_month - 1]

    # Growth rate
    if last_revenue > 0:
        growth_rate = ((current_revenue - last_revenue) / last_revenue) * 100
    else:
        growth_rate = 0

    # Appointments this month
    from app.models import Appointments  # Replace with your actual model
    appointments_this_month = db.session.query(func.count(Appointments.appointment_id))\
        .filter(extract('month', Appointments.appointment_sched) == current_month)\
        .filter(extract('year', Appointments.appointment_sched) == current_year)\
        .scalar()

    # Top earning services
    service_month_data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        Procedures.treatment_procedure,
        func.sum(Transactions.total_amount_paid).label('total')
    ).join(Procedures, Procedures.procedure_id == Transactions.procedure_id)\
    .filter(extract('year', Transactions.transaction_datetime) == selected_year)\
    .group_by('month', Procedures.treatment_procedure)\
    .order_by('month')\
    .all()

    # Example: {'Cleaning': [1000, 1500, 0, ..., 2000], 'Whitening': [...], ...}
    service_monthly_totals = defaultdict(lambda: [0]*12)

    for month, service, total in service_month_data:
        service_monthly_totals[service][int(month) - 1] = float(total)

    # Convert to chart.js dataset format
    stacked_datasets = [{
        'label': service,
        'data': totals
    } for service, totals in service_monthly_totals.items()]

    # Color generator (optional)
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1',
            '#17a2b8', '#6610f2', '#fd7e14', '#20c997', '#6c757d']

    for i, ds in enumerate(stacked_datasets):
        ds['backgroundColor'] = colors[i % len(colors)]

    # --- BUSINESS INSIGHT BASED ONLY ON CURRENT DATA ---
    insight_lines = []

    # Insight 1: Appointment count
    appointment_insight = ["<strong>Appointments:</strong>"]
    if appointments_this_month < 10:
        appointment_insight.append("Appointment volume is low. Consider sending reminders or running promotions.")
    elif appointments_this_month < 20:
        appointment_insight.append("Appointment count is moderate. You may benefit from increased engagement.")
    else:
        appointment_insight.append("Great job! You have a healthy number of appointments this month.")
    insight_lines.append("<br>".join(appointment_insight))

    # Insight 2: Revenue performance
    revenue_insight = ["<strong>Revenues:</strong>"]
    if current_revenue < 10000:
        revenue_insight.append("Revenue is below ₱10,000. Review pricing or promote top services.")
    elif current_revenue < 20000:
        revenue_insight.append("Revenue is fair. Highlight best-sellers to boost earnings.")
    else:
        revenue_insight.append("Strong revenue this month! Keep up the momentum.")
    insight_lines.append("<br>".join(revenue_insight))

    # Insight 3: Top services
    # Filter to current month only
    current_month_services = [
        entry for entry in service_month_data if int(entry.month) == current_month
    ]

    # Find the top earning service this month
    top_service_this_month = None
    if current_month_services:
        top_service_this_month = max(current_month_services, key=lambda x: x.total)

    service_insight = ["<strong>Services:</strong>"]
    if top_service_this_month:
        service_insight.append(
            f"Top earning service this month: {top_service_this_month.treatment_procedure}. Consider upselling related procedures."
        )
    else:
        service_insight.append("No services recorded yet this month.")
    insight_lines.append("<br>".join(service_insight))

    insight_text = "<br><br>".join(insight_lines)

    return render_template('/owner/reports.html',
                           labels=months,
                           today_revenue=today_revenue,
                           values=values,
                           total_revenue=sum(values),
                           current_revenue=current_revenue,
                            selected_year=selected_year,
                            current_year=current_year,
                           growth_rate=round(growth_rate, 2),
                           appointments_count=appointments_this_month,
                           stacked_datasets=stacked_datasets,
                           insight_text=insight_text)

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

