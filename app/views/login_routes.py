from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.accounts import Account
from datetime import timedelta

login = Blueprint('login', __name__, template_folder='../templates')
login.permanent_session_lifetime = timedelta(minutes=15)

@login.route('/', methods=['GET'])
def login_page():
    return render_template('/login_page/login.html')

@login.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    account_password = request.form.get('password')
    
    account = Account.query.filter_by(email=email).first()
    
    print("DB hashed password:", account.account_password)
    print("Entered password:", account_password)
    
    if not account or account.account_password != account_password:
        flash("Invalid email or password", "error")
        return redirect(url_for('login.login_page'))
    
    session.permanent = True
    session['user_id'] = account.account_id
    session['email'] = account.email
    session['access_level'] = account.access_level
    
    if account.access_level == 'owner':
        return redirect(url_for('owner.owner_home'))
    elif account.access_level == 'staff':
        return redirect(url_for('staff.staff_home'))
    
    flash("Access level not recognized.", "error")
    return redirect(url_for('login.login_page'))
    
@login.route('/register')
def register():
    return render_template('/login_page/register.html')