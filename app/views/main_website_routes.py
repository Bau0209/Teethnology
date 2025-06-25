from flask import Blueprint, render_template
from app.models.branches import Branch

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    branches = Branch.query.all()
    return render_template('/main_website/Home.html', branches=branches)

@main.route('/contact')
def contact():
    return render_template('/main_website/contact.html')

@main.route('/form')
def form():
    return render_template('/main_website/form.html')

@main.route('/branch')
def branch():
    return render_template('/main_website/branch.html')

