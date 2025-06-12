from flask import Blueprint, render_template

staff = Blueprint('staff', __name__)

@staff.route('/')
def staff_home():
    return "Staff homepage"
