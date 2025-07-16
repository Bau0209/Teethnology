from flask import Blueprint, session
from app.utils.auth import restrict_roles

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def restrict_dashboard_access():
    # Call the reusable function
    return restrict_roles(['owner', 'staff'])

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
    report_routes
)
