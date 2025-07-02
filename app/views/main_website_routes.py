from flask import Blueprint, render_template
from app.models import Branch, ClinicBranchImage, MainWeb

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    branches = Branch.query.all()
    main_web = MainWeb.query.first()
    return render_template('/main_website/Home.html', branches=branches, main_web=main_web)

@main.route('/contact')
def contact():
    main_web = MainWeb.query.first()
    branches = Branch.query.all()
    return render_template('/main_website/contact.html', branches=branches, main_web=main_web)

@main.route('/form')
def form():
    return render_template('/main_website/form.html')

@main.route('/branch/<int:branch_id>')
def branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch_images = ClinicBranchImage.query.filter_by(branch_id=branch_id).all()
    return render_template('/main_website/branch.html', branch=branch, branch_images=branch_images)
