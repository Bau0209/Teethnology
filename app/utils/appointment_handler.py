from flask import render_template, request, flash, redirect
from app.models import Appointments, PatientsInfo
from app import db
from datetime import datetime, timedelta

#Appointment Booking functions
def safe_input(key):
    return request.form.get(key, '').strip()

def create_appointment(branch_id, patient_id, date, time, appointment_type, returning):
    appointment = Appointments(
        branch_id=branch_id,
        patient_id=patient_id,
        appointment_date=date,
        appointment_time=time,
        appointment_type=appointment_type,
        appointment_status='pending',
        returning_patient=returning
    )
    db.session.add(appointment)
    db.session.commit()
    
def check_schedule_conflict(branch_id, preferred_sched, buffer_minutes=30):
    start_range = preferred_sched - timedelta(minutes=buffer_minutes)
    end_range = preferred_sched + timedelta(minutes=buffer_minutes)
    return Appointments.query.filter(
        Appointments.branch_id == branch_id,
        Appointments.appointment_sched > start_range,
        Appointments.appointment_sched < end_range
    ).first()

def handle_appointment_form(template_path):
    if request.method == 'POST':
        is_returning = request.form.get('firstvisit') == 'yes'
        first_name = safe_input('first_name').lower()
        last_name = safe_input('last_name').lower()
        branch_id = int(request.form.get('branch_id'))

        # Convert 'male'/'female' to 'M'/'F'
        raw_gender = safe_input('sex').lower()
        sex = 'M' if raw_gender == 'male' else 'F' if raw_gender == 'female' else None

        # Parse appointment_date and appointment_time safely
        try:
            date_str = request.form.get('appointment_date')
            time_str = request.form.get('appointment_time')
            appointment_sched = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            flash("Invalid appointment date or time format.", "danger")
            return redirect(request.referrer)

        if check_schedule_conflict(branch_id, appointment_sched):
            flash("This time slot is already booked. Please choose a different schedule.", "warning")
            return redirect(request.referrer)

        appointment_type = request.form.get('appointment_type')

        if is_returning:
            # Validate returning patient by ID and name
            patient_id = int(request.form.get('patient_id'))
            patient = PatientsInfo.query.filter_by(patient_id=patient_id).first()
            if not patient or patient.first_name.lower() != first_name or patient.last_name.lower() != last_name:
                flash("Invalid Patient ID or Name. Please try again.", "danger")
                flash(f"Entered ID: {patient_id}", "danger")
                flash(f"Entered Name: {first_name.title()} {last_name.title()}", "danger")
                if patient:
                    flash(f"DB Name: {patient.first_name.title()} {patient.last_name.title()}", "danger")
                else:
                    flash("No patient found with that ID.", "danger")
                return redirect(request.referrer)

            # Create appointment for returning patient
            create_appointment(branch_id, patient.patient_id, date_str, time_str, appointment_type, returning=True)
            flash("Appointment booked successfully for returning patient.", "success")
            return redirect(request.referrer)

        else:
            # Register new patient
            new_patient = PatientsInfo(
                branch_id=branch_id,
                first_name=safe_input('first_name'),
                middle_name=safe_input('middle_name'),
                last_name=safe_input('last_name'),
                birthdate=request.form.get('dob'),
                sex=sex,
                contact_number=safe_input('contact'),
                email=safe_input('email'),
                address_line1=safe_input('address_line1'),
                baranggay=safe_input('baranggay'),
                city=safe_input('city'),
                province=safe_input('province'),
                country=safe_input('country'),
                initial_consultation_reason=appointment_type
            )
            db.session.add(new_patient)
            db.session.commit()

            # Create appointment for new patient
            create_appointment(branch_id, new_patient.patient_id, date_str, time_str, appointment_type, returning=False)
            flash("Appointment booked successfully for new patient.", "success")
            return redirect(request.referrer)

    return render_template(template_path)

#--------------------
#Dashboard data
def get_appointments_by_date(target_date, branch_id=None):
    query = Appointments.query.filter(db.func.date(Appointments.appointment_date) == target_date)
    if branch_id:
        query = query.filter(Appointments.branch_id == branch_id)
    return query.all()

def get_pending_appointments(branch_id=None):
    query = Appointments.query.filter_by(appointment_status='pending')
    if branch_id:
        query = query.filter(Appointments.branch_id == branch_id)
    return query.order_by(Appointments.appointment_date.asc()).all()