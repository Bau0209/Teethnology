from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.views.dashboard import dashboard
from app.models import Account
from functools import wraps
import logging
import re

# Set up logging
logger = logging.getLogger(__name__)

def login_required(f):
    """Decorator to ensure user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    """Decorator to require owner access level"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('access_level') != 'owner':
            flash('Owner privileges required', 'error')
            logger.warning(f'Unauthorized access attempt by user {session.get("user_id")}')
            return redirect(url_for('dashboard.owner_home' if session.get('access_level') == 'owner' else 'dashboard.staff_home'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    """Security settings page for both owners and staff"""
    try:
        if request.method == 'POST':
            return handle_password_change()
        
        return render_template('dashboard/security.html', 
                           access_level=session.get('access_level'))
    
    except Exception as e:
        logger.error(f"Error in security route: {str(e)}", exc_info=True)
        flash('An error occurred while processing your request', 'error')
        return redirect(url_for('dashboard.owner_home' if session.get('access_level') == 'owner' else 'dashboard.staff_home'))

def validate_password_strength(password):
    """Validate password meets strength requirements"""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain at least one lowercase letter'
    
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least one number'
    
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, 'Password must contain at least one special character'
    
    return True, ''

def handle_password_change():
    """Handle password change form submission"""
    if session.get('access_level') != 'owner':
        flash('Only owners can change passwords', 'error')
        logger.warning(f'Password change attempt by non-owner user {session.get("user_id")}')
        return redirect(url_for('dashboard.security'))
    
    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')
    
    # Validate inputs
    if not all([current_password, new_password, confirm_password]):
        flash('All fields are required', 'error')
        return redirect(url_for('dashboard.security'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('dashboard.security'))
    
    # Validate password strength
    is_valid, message = validate_password_strength(new_password)
    if not is_valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.security'))
    
    # Get account from database
    account = Account.query.get(session.get('user_id'))
    if not account:
        flash('Account not found', 'error')
        session.clear()
        return redirect(url_for('login.login_page'))
    
    # Verify current password using hashed password
    if not check_password_hash(account.account_password, current_password):
        flash('Current password is incorrect', 'error')
        logger.warning(f'Incorrect current password attempt by user {session.get("user_id")}')
        return redirect(url_for('dashboard.security'))
    
    # Check if new password is different from current
    if check_password_hash(account.account_password, new_password):
        flash('New password must be different from current password', 'error')
        return redirect(url_for('dashboard.security'))
    
    # Update password with hashed version
    try:
        account.account_password = generate_password_hash(new_password)
        db.session.commit()
        logger.info(f'Password successfully changed for user {session.get("user_id")}')
        
        # Optional: Invalidate other sessions here
        # session['password_changed'] = True
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard.security'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating password for user {session.get('user_id')}: {str(e)}", exc_info=True)
        flash('Failed to update password. Please try again.', 'error')
        return redirect(url_for('dashboard.security'))