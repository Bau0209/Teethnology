from flask import request, flash, redirect, render_template, url_for
from datetime import date, datetime

from app.views.dashboard import dashboard
from app.models import Employee, Branch, Account
from app import db

@dashboard.route('/employees', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard.employees', branch=selected_branch))

    # --- Handle GET: fetch employees based on selected branch ---
    if selected_branch == 'all':
        employees = Employee.query.all()
    else:
        employees = Employee.query.filter_by(branch_id=selected_branch).all()

    return render_template('/dashboard/employees.html', 
                           branches=branches, 
                           selected_branch=selected_branch,
                           employees=employees, 
                           employee=None,
                           today=date.today())

@dashboard.route('/employee_info/<int:employee_id>')
def employee_info(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/dashboard/employee_basic_info.html', employee=employee)

@dashboard.route('/employee_work_details/<int:employee_id>')
def employee_work_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)    
    account = Account.query.filter_by(employee_id=employee_id).first()
    return render_template('/dashboard/employee_work_details.html', employee=employee, account=account)

@dashboard.route('/edit_employee/<int:employee_id>', methods=['POST'])
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
        return redirect(url_for('dashboard.employee_info', employee_id=employee_id))
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
        return redirect(url_for('dashboard.employee_work_details', employee_id=employee_id))

@dashboard.route('/employee_activity_details/<int:employee_id>')
def employee_activity_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('/owner/o_em_activity_details.html', employee=employee)
