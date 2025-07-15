from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

# Import route modules to attach them to the blueprint
from . import branch_routes, home_routes