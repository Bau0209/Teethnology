from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Account, Employee
from werkzeug.security import generate_password_hash
from datetime import timedelta
from app import db

login = Blueprint('login', __name__, template_folder='../templates')

@login.route('/', methods=['GET'])
def login_page():
    return render_template('/login_page/login.html')

@login.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    account_password = request.form.get('password')
    
    account = Account.query.filter_by(email=email).first()

    if not account or account.account_password != account_password:
        flash("Invalid email or password", "error")
        return redirect(url_for('login.login_page'))
    
    session.permanent = True
    session['user_id'] = account.account_id
    session['email'] = account.email
    session['access_level'] = account.access_level
    session.permanent = True
    
    if account.access_level == 'owner':
        return redirect(url_for('owner.owner_home'))
    elif account.access_level == 'staff':
        return redirect(url_for('staff.staff_home'))
    
    flash("Access level not recognized.", "error")
    return redirect(url_for('login.login_page'))
    

@login.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Safely extract form data
        employee_id = request.form.get('employee-id')
        first_name = request.form.get('first-name', '').strip()
        middle_name = request.form.get('middle-name', '').strip()
        last_name = request.form.get('last-name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')

        # Validate all required fields
        if not all([employee_id, first_name, last_name, email, password, password_confirm]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('login.register'))

        # Password match validation
        if password != password_confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('login.register'))

        # Email uniqueness check
        existing_account = Account.query.filter_by(email=email).first()
        if existing_account:
            flash("Email already registered.", "danger")
            return redirect(url_for('login.register'))

        # Check if employee exists
        employee = Employee.query.filter_by(
            employee_id=employee_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        ).first()

        if not employee:
            flash("Employee record not found. Please contact admin.", "danger")
            return redirect(url_for('login.register'))

        # Check if employee already has an account
        existing_linked_account = Account.query.filter_by(employee_id=employee.employee_id).first()
        if existing_linked_account:
            flash("This employee already has an account.", "danger")
            return redirect(url_for('login.register'))

        # Create new account
        hashed_password = generate_password_hash(password)
        new_account = Account(
            employee_id=employee.employee_id,
            email=email,
            account_password=hashed_password,
            access_level='staff',
            account_status='active'
        )
        db.session.add(new_account)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login.login_page'))

    return render_template('/login_page/register.html')

@login.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login.login_page'))