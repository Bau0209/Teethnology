from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from app.models import Branch, ClinicBranchImage, MainWeb, PatientsInfo, Appointments
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    branches = Branch.query.all()
    main_web = MainWeb.query.first()
    return render_template('/main_website/Home.html', branches=branches, main_web=main_web)

@main.route('/contact')
def contact():
    main_web = MainWeb.query.first()
    branches = Branch.query.all()
    return render_template('/main_website/contact.html', branches=branches, main_web=main_web)

@main.route('/form', methods=['GET', 'POST'])
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
            return redirect(url_for('main.form'))

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
            return redirect(url_for('main.form'))

    return render_template('/main_website/form.html', branches=branches)

@main.route('/branch/<int:branch_id>')
def branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/main_website/branch.html', branch=branch, branch_images=branch_images)

@main.route('/api/services')
def get_services():
    services = MainWeb.query.all()
    return jsonify([
        {
            "name": s.name,
            "description": s.description,
            "icon_class": s.icon_class,         # Example: 'fas fa-tooth'
            "bg_image": s.bg_image              # Example: '/static/images/tooth-bg.png'
        } for s in services
    ])
