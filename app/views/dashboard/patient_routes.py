from flask import request, render_template, redirect, flash, url_for, session, jsonify

from app import db
from app.models import Branch, PatientsInfo, PatientMedicalInfo, DentalInfo, Procedures
from app.views.dashboard import dashboard
from datetime import datetime, date

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return None   

@dashboard.route('/patients')
def patients():
    access_level = session.get('access_level')
    access_branch_id = session.get('access_branch')

    # Get actual Branch object
    access_branch = Branch.query.get(access_branch_id)

    # Get branch filter from query string (if any)
    selected_branch = request.args.get('branch', 'all')

    # If staff, override selected_branch with their own branch_id
    if access_level == 'staff':
        selected_branch = access_branch_id

    # Fetch patients based on selected branch
    if selected_branch == 'all':
        patients = PatientsInfo.query.all()
    else:
        patients = PatientsInfo.query.filter_by(branch_id=selected_branch).all()

    branches = Branch.query.all()

    return render_template(
        '/dashboard/patients.html',
        patients=patients,
        patient=None,
        patient_medical_info=None,
        dental_record=[],
        branches=branches,
        selected_branch=selected_branch,
        access_level=access_level,
        access_branch=access_branch.branch_name
    )

@dashboard.route('/patients/add', methods=['POST'])
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
        return redirect(url_for('dashboard.patients'))
    
    except Exception as e:
        error_message = str(e)
        # Instead of redirecting, re-render the form with error
        return render_template(
            '/dashboard/patients.html',
            error_message=error_message,
            patients=[],  # or existing data if needed
            patient=None,
            patient_medical_info=None,
            dental_record=[],
            branches=Branch.query.all(),
            selected_branch='all'
        )
 
@dashboard.route('/edit_patient/<patient_id>', methods=['GET', 'POST'])
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
            
            return redirect(url_for('dashboard.edit_patient', patient_id=patient_id))

    # GET request
    return render_template(
        'dashboard/patient_info.html',
        patient=patient,
        dental_record=dental_record,
        patient_medical_info=patient_medical_info,
        current_date=datetime.today().date()
    )

@dashboard.route('/patient_info/<patient_id>')
def patient_info(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id) 
    patient_medical_info = PatientMedicalInfo.query.get(patient_id) 
    dental_info = DentalInfo.query.get(patient_id)  

    return render_template(
        '/dashboard/patient_info.html',
        patient=patient,
        patient_medical_info=patient_medical_info,
        dental_info=dental_info
    )

@dashboard.route('/patient_procedure/<patient_id>') 
def patient_procedure(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    procedures = Procedures.query.filter_by(patient_id=patient_id)
    return render_template('/dashboard/procedure.html',patient=patient, procedures=procedures)

@dashboard.route('/patient_dental_rec/<patient_id>')   
def patient_dental_rec(patient_id):
    patient = PatientsInfo.query.get_or_404(patient_id)
    dental_record = DentalInfo.query.filter_by(patient_id=patient_id)
    return render_template(
        '/dashboard/dental_record.html', 
        patient=patient, 
        dental_record=dental_record)
