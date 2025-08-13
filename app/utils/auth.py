from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for('login.login_page'))
            if session.get('access_level') not in roles:
                flash("Access denied.", "danger")
                return redirect(url_for('login.login_page'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def restrict_roles(allowed_roles):
    if 'user_id' not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for('login.login_page'))

    if session.get('access_level') not in allowed_roles:
        flash("Access denied.", "danger")
        return redirect(url_for('login.login_page'))

    return None  # continue with the request
