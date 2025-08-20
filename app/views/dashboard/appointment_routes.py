from flask import request, render_template, session, jsonify, flash, redirect, url_for
from datetime import date, datetime
from sqlalchemy import func
from werkzeug.utils import secure_filename

import traceback
import json, os

from app.models import Procedures, Appointments
from app import db

from app.views.dashboard import dashboard
from app.models import Appointments, Branch, InventoryItem, PatientsInfo, Archive
from app.utils import appointment_handler as ah
from app.utils import procedure_handler as ph
from app.utils import inventory_handler as ih

@dashboard.route("/api/branches")
def get_branches():
    branches = Branch.query.all()
    return jsonify([{"id": b.branch_id, "name": b.branch_name} for b in branches])

@dashboard.route('/appointments')
def appointments():
    inventory_items = InventoryItem.query.filter(InventoryItem.category != 'Equipment').all()
    selected_branch = request.args.get('branch', 'all')
    appointment_id = request.args.get('appointment_id')

    query = Appointments.query

    if selected_branch != 'all':
        query = query.filter_by(branch_id=selected_branch)

    if appointment_id:
        query = query.filter_by(appointment_id=appointment_id)

    appointments = query.filter(Appointments.appointment_status != 'cancelled').all()
    branches = Branch.query.all()

    events = [
        {
            'title': f"{a.patient.patient_full_name} - {a.appointment_type}",
            'start': a.appointment_date.strftime('%Y-%m-%d'),
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
            'branch_id': a.branch.branch_id,
            'branch_name': a.branch.branch_name,
            'appointment_id': a.appointment_id,
            'status': a.appointment_status,
            'time': a.appointment_time.strftime('%I:%M %p'),
            'reason': a.appointment_type,
            'patient_name': a.patient.patient_full_name,
            'patient_type': 'Returning Patient' if a.returning_patient else 'New Patient',
            'contact': a.patient.contact_number,
            'email': a.patient.email,'date': a.appointment_date.strftime('%Y-%m-%d'),
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
        inventory_items=inventory_items,
        branches=branches,
        appointments=appointments,
        selected_branch=selected_branch,
        events=json.dumps(events),
        appointment_data=json.dumps(appointment_data)
    )

@dashboard.route('/appointment_req')
def appointment_req():
    selected_branch = request.args.get('branch', 'all')
    
    appointments = Appointments.query.filter_by(appointment_status='Pending').order_by(Appointments.appointment_date.asc()).all()

    if selected_branch != 'all':
        appointments = appointments.filter_by(branch_id=selected_branch).order_by(Appointments.appointment_date.asc()).all()

    appointment_data = [
        {
            'date': a.appointment_date.strftime('%Y-%m-%d'),
            'time': a.appointment_date.strftime('%I:%M %p'),        
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

@dashboard.route('/appointment_archives')
def appointment_archives():
    selected_branch = request.args.get('branch', 'all')
    appointments = Appointments.query.filter_by(appointment_status='Cancelled').order_by(Appointments.appointment_date.asc()).all()

    if selected_branch != 'all':
        appointments = appointments.filter_by(branch_id=selected_branch).order_by(Appointments.appointment_date.asc()).all()
        
    appointment_data = [
        {
            'date': a.appointment_date.strftime('%Y-%m-%d'),
            'time': a.appointment_date.strftime('%I:%M %p'),        
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
        'dashboard/appointment_archives.html',
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
            preferred_raw = request.form.get('preferred')
            preferred_dt = datetime.fromisoformat(preferred_raw)
            
            new_appointment = Appointments(
                branch_id=branch_id,
                patient_id=patient.patient_id,
                appointment_date=preferred_dt.date(),
                appointment_time=preferred_dt.time(),
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
                patient_id=ah.generate_patient_id(),
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
            
            preferred_raw = request.form.get('preferred')
            preferred_dt = datetime.fromisoformat(preferred_raw)
            
            new_appointment = Appointments(
                branch_id=branch_id,
                patient_id=new_patient.patient_id,
                appointment_date=preferred_dt.date(),
                appointment_time=preferred_dt.time(),
                appointment_type=request.form.get('appointment_type'),
                appointment_status='pending',
                returning_patient=False
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment booked successfully for new patient.", "success")
            return redirect(url_for('dashboard.appointments'))

    return render_template('/dashboard/appointment.html', branches=branches)

@dashboard.route("/appointment/inventory/<int:branch_id>")
def get_inventory_by_branch(branch_id):
    inventory_items = InventoryItem.query.filter(
        InventoryItem.branch_id == branch_id,
        func.lower(InventoryItem.category) != 'equipment'
    ).all()

    return jsonify([
        {
            "id": item.item_id,
            "item_name": item.item_name,
            "quantity_unit": item.quantity_unit
        }
        for item in inventory_items
    ])

@dashboard.route('/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    try:
        data = request.get_json()
        status = data.get('status')
        print(f"[DEBUG] Appointment ID: {appointment_id}, Status: {status}")

        # Validate status
        if status not in ['approved', 'cancelled', 'completed']:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400

        appointment = Appointments.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'message': 'Appointment not found'}), 404

        # Update appointment status
        appointment.appointment_status = status

        # Update procedures (if any)
        if status == 'completed':
            procedures = Procedures.query.filter_by(appointment_id=appointment_id).all()

            if not procedures and not data.get('allowWithoutProcedure', False):
                return jsonify({'success': False, 'message': 'No procedure records found for this appointment'}), 404

            for proc in procedures:
                proc.procedure_status = status

        try:
            db.session.commit()
        except Exception as commit_err:
            db.session.rollback()
            print(f"[Commit Error] {commit_err}")
            return jsonify({'success': False, 'message': 'Error saving changes.', 'error': str(commit_err)}), 500

        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        print("[ERROR] Exception in update_appointment_status:", e)
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Internal Server Error', 'error': str(e)}), 500

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

    appointment = ah.get_appointment(appointment_id)
    if not appointment:
        return redirect(url_for('appointment.branches'))

    # Create procedure
    procedure = ph.create_procedure(
        appointment_id=appointment.appointment_id,
        appointment_date=appointment.appointment_date,
        treatment_procedure=treatment_procedure,
        tooth_area=tooth_area,
        provider=provider,
        treatment_plan=treatment_plan,
        fee=fee
    )

    # Handle receipt upload
    receipt_path = ah.save_receipt_file(receipt_file)

    # Create transaction
    ph.create_transaction(
        procedure_id=procedure.procedure_id,
        treatment_procedure=treatment_procedure,
        provider=provider,
        payment_method=payment_method,
        total_paid=total_paid,
        receipt_path=receipt_path
    )

    # Update procedure history
    procedure_history = ah.mark_procedure_history_completed(appointment.appointment_id)
    
    # Create Inventory Usage Records
    for item_id_str, qty_str in request.form.items():
        if item_id_str.startswith("quantity_used["):
            # Extract the inventory_item_id from the key
            inventory_item_id = item_id_str.split("[")[1].split("]")[0]
            quantity_used = float(qty_str or 0)

            if quantity_used > 0:  # only record if actually used
                ih.create_inventory_usage_record(
                    procedure_id=procedure.procedure_id,
                    inventory_item_id=inventory_item_id,
                    quantity_used=quantity_used
                )

    
    db.session.commit()
    flash("Procedure, transaction, and procedure history updated!", "success")
    return redirect(url_for('dashboard.appointments', success=1))

@dashboard.route('/edit_appointment/<int:id>', methods=['POST'])
def edit_appointment(id):
    from datetime import datetime

    # Find the appointment by ID first
    appt = Appointments.query.get_or_404(id)
    patient = appt.patient

    # Get form data
    branch_id = request.form.get('branch')
    patient_name = request.form.get('patient-name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    reason = request.form.get('reason')
    date = request.form.get('edit-initial-date')
    time = request.form.get('edit-initial-time')

    # Update patient info (only if provided)
    if patient_name:
        patient.patient_name = patient_name
    if contact:
        patient.contact_number = contact
    if email:
        patient.email = email

    new_datetime = request.form.get('new_appointment_datetime') 
    
    # Update appointment datetime
    if new_datetime:
        print("DEBUG new_appointment_datetime =", new_datetime)
        dt = datetime.strptime(new_datetime, "%Y-%m-%dT%H:%M")
        appt.appointment_date = dt.date()
        appt.time = dt.time()
    else:
        if date:
            appt.appointment_date = date
        if time:
            appt.time = time

    # Update branch
    if branch_id:
        branch = Branch.query.filter_by(branch_id=branch_id).first()
        if not branch:
            flash("Branch not found!", "danger")
            return redirect(url_for('dashboard.appointments', success=1))
        appt.branch_id = branch.branch_id
        appt.branch_name = branch.branch_name

    # Update reason (if provided)
    if reason:
        appt.appointment_type = reason

    # Save changes
    db.session.commit()

    flash("Appointment updated successfully!", "success")
    return redirect(url_for('dashboard.appointments', success=1))

@dashboard.route('/cancel_appointment/<int:id>', methods=['POST'])
def cancel_appointment(id):
    appointment = db.session.query(Appointments).get(id)
    if appointment:
        appointment.appointment_status = 'cancelled'
        db.session.commit()  # This is critical!
        return jsonify(success=True)
    return jsonify(success=False, message="Appointment not found"), 404

@dashboard.route('/patients/<int:patient_id>/archive', methods=['POST'])
def archive_patient(patient_id):
    patient = PatientsInfo.query.get(patient_id)
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404

    archive_record = Archive(
        original_id=patient.patient_id,
        table_name='patients',
        archived_data=json.dumps(patient.as_dict(), default=str),
        archived_by=session.get('user', 'admin'),
        timestamp=datetime.utcnow()
    )

    db.session.add(archive_record)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'success': True})