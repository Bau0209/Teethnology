from flask import request, render_template, session, jsonify, flash, redirect, url_for, current_app
from app.models import Account, Employee
from app import db

from app.views.dashboard import dashboard


@dashboard.route('/account')
def account_page():
    if 'user_id' not in session:
        flash("You must be logged in to view this page.", "danger")
        return redirect(url_for('login.login_page'))

    account = Account.query.get(session['user_id'])

    if not account:
        flash("Account not found.", "danger")
        return redirect(url_for('login.login_page'))

    employee = account.employee

    user_data = {
        'name': f"{employee.first_name} {employee.middle_name or ''} {employee.last_name}",
        'contact': employee.contact_no,
        'email': account.email,
        'access_level': account.access_level,
        'age': employee.age,
        'gender': employee.gender,
        'birthday': employee.birth_date,
        'branch': employee.branch.branch_name if employee.branch else "N/A",
        'date_hired': employee.date_hired,
        'license_number': employee.license_number,
        'department': employee.department,
        'shift_schedule': employee.shift_schedule
    }

    return render_template(
        'dashboard/account.html',
        access_level=session.get('access_level'),
        user=user_data
    )
