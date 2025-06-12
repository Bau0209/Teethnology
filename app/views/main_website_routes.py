from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('/main_website/Home.html')

@main.route('/contact')
def contact():
    return render_template('/main_website/contact.html')

@main.route('/form')
def form():
    return render_template('/main_website/form.html')