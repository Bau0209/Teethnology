from flask import Blueprint, render_template

login = Blueprint('login', __name__)

@login.route('/')
def gateway():
    return render_template('/login_page/portal_gateway.html')

@login.route('/login')
def login_page():
    return render_template('/login_page/login.html')

@login.route('/register')
def register():
    return render_template('/login_page/register.html')