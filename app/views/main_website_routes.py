from flask import Blueprint, render_template, jsonify
from app.models import Branch, ClinicBranchImage, MainWeb
from app.utils.appointment_handler import handle_appointment_form
from app.utils.branch_handler import get_first_branch_images

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    branch_images = get_first_branch_images()
    return render_template('/main_website/Home.html', branch_images=branch_images)

@main.route('/contact')
def contact():
    return render_template('/main_website/contact.html')

@main.route('/branch/<int:branch_id>')
def branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/main_website/branch.html', branch=branch, branch_images=branch_images)

@main.route('/api/services')
def get_services():
    services = MainWeb.query.all()
    return jsonify([
        {
            "name": s.name,
            "description": s.description,
            "icon_class": s.icon_class,         # Example: 'fas fa-tooth'
            "bg_image": s.bg_image              # Example: '/static/images/tooth-bg.png'
        } for s in services
    ])

@main.route('/form', methods=['GET', 'POST'])
def form():
    return handle_appointment_form('/main_website/form.html')

@main.app_context_processor
def inject_common_data():
    return {
        "branches": Branch.query.all(),
        "main_web": MainWeb.query.first()
    }
