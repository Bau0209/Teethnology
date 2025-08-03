from flask import request, render_template, session, jsonify, flash, redirect, url_for, current_app
from datetime import date, datetime
from werkzeug.utils import secure_filename

import json, os

from app.models import Procedures
from app import db

from app.views.dashboard import dashboard
from app.models import Appointments, Branch, Transactions, PatientsInfo

@dashboard.route('/appointments')
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
        'dashboard/appointment.html',
        branches=branches,
        appointments=appointments,
        selected_branch=selected_branch,
        events=json.dumps(events),
        appointment_data=json.dumps(appointment_data)
    )

@dashboard.route('/appointment_req')
def appointment_req():
    selected_branch = request.args.get('branch', 'all')
    
    appointments = Appointments.query.filter_by(appointment_status='Pending').order_by(Appointments.appointment_sched.asc()).all()

    if selected_branch != 'all':
        appointments = appointments.filter_by(branch_id=selected_branch).order_by(Appointments.appointment_sched.asc()).all()

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
        'dashboard/appointment_request.html',
        branches=branches,
        appointments=appointments,
        selected_branch=selected_branch,
        appointment_data=json.dumps(appointment_data)
    )

#Adding an Appointment in the calendar
@dashboard.route('/form', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard.appointments'))

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
            return redirect(url_for('dashboard.appointments'))

    return render_template('/dashboard/appointment.html', branches=branches)

@dashboard.route('/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    data = request.get_json()
    status = data.get('status')

    appointment = Appointments.query.get_or_404(appointment_id)
    appointment.status = status
    db.session.commit()
    return jsonify(success=True)

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
        if not procedures and not data.get('allowWithoutProcedure', False):
            return jsonify({'success': False, 'message': 'No procedure records found for this appointment'}), 404

        for proc in procedures:
            proc.procedure_status = status

    db.session.commit()

    return jsonify({'success': True, 'message': 'Status updated successfully'})

@dashboard.route('/appointment/complete', methods=['POST'])
def complete_appointment():
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
        return redirect(url_for('appointment.branches'))

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
    return redirect(url_for('dashboard.appointments'))

