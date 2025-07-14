from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

db = SQLAlchemy()
load_dotenv()

def create_app():
    # Load environment variables from .env
    print("User:", os.environ.get('DB_USER'))
    print("Password:", os.environ.get('DB_PASSWORD'))
    print("Host:", os.environ.get('DB_HOST'))
    print("Database:", os.environ.get('DB_NAME'))

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/branches'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB
    db.init_app(app)
    
    # Import blueprints from views
    from app.views import main, owner, staff, login

    app.register_blueprint(main)
    app.register_blueprint(owner, url_prefix='/owner')
    app.register_blueprint(staff, url_prefix='/staff')
    app.register_blueprint(login, url_prefix='/login')    

    return app