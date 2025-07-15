from flask import render_template, request, redirect, url_for, flash, session
from datetime import date, timedelta

from app.views.dashboard import dashboard
from app.utils.auth import role_required
from app.models import Branch, MainWeb, Appointments
from app.utils.appointment_handler import get_appointments_by_date, get_pending_appointments
from app.utils.insights import generate_business_insight
from app import db

@dashboard.route('/owner_home')
# @role_required('owner')
def owner_home():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    selected_branch = request.args.get('branch', 'all')
    branch_id = int(selected_branch) if selected_branch != 'all' else None

    branches = Branch.query.all()
    main_web = MainWeb.query.first()

    appointments_today = get_appointments_by_date(today, branch_id)
    appointments_tomorrow = get_appointments_by_date(tomorrow, branch_id)
    appointment_requests = get_pending_appointments(branch_id)

    insight_text = generate_business_insight()

    return render_template(
        '/dashboard/owner_home.html',
        appointments_today=appointments_today,
        appointments_tomorrow=appointments_tomorrow,
        appointment_requests=appointment_requests,
        branches=branches,
        selected_branch=selected_branch,
        main_web=main_web,
        insight_text=insight_text
    )
    
@dashboard.route('/staff_home')
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
        '/dashboard/staff_home.html',
        appointments_today=appointments_today,
        appointments_tomorrow=appointments_tomorrow,
        appointment_requests=appointment_requests,
        branches=branches,
        selected_branch=selected_branch,
        main_web=main_web,
        insight_text=insight_text
    )
    
@dashboard.route('/update-main-website', methods=['POST'])
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
    return redirect(url_for('dashboard.owner_home'))

