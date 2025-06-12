from flask import Blueprint, render_template

owner = Blueprint('owner', __name__)

@owner.route('/')
def owner_home():
    return "Owner homepage"
