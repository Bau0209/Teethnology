from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Import blueprints from views
    from app.views import main, owner, staff, login

    app.register_blueprint(main)
    app.register_blueprint(owner, url_prefix='/owner')
    app.register_blueprint(staff, url_prefix='/staff')
    app.register_blueprint(login, url_prefix='/login')

    return app