from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for('login.login_page'))
            if session.get('access_level') != role:
                flash("Access denied.", "danger")
                return redirect(url_for('login.login_page'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
