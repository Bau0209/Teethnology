from flask import Blueprint, session, current_app
from ...utils import archive_function
from app.utils.auth import restrict_roles
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def restrict_dashboard_access():
    # Call the reusable function
    return restrict_roles(['owner', 'staff'])

# Define the filter function
def format_date(value):
    if isinstance(value, datetime):
        return value.strftime('%B %d, %Y')
    return value

# Register the filter — must be done after `dashboard` is defined
@dashboard.before_app_request
def register_template_filters():
    current_app.jinja_env.filters['format_date'] = format_date

@dashboard.context_processor
def inject_access_level():
    return {
        'access_level': session.get('access_level')
    }

# Import route modules
from . import (
    branch_routes, 
    home_routes, 
    appointment_routes, 
    patient_routes, 
    employee_routes, 
    inventory_routes,
    transaction_routes,
    report_routes, 
    accounts_routes,
    security_routes
)
