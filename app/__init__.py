from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import os
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    # Debug prints
    print("User:", os.environ.get('DB_USER'))
    print("Password:", os.environ.get('DB_PASSWORD'))
    print("Host:", os.environ.get('DB_HOST'))
    print("Database:", os.environ.get('DB_NAME'))

    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.permanent_session_lifetime = timedelta(minutes=15)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/branches'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    db.init_app(app)
    migrate.init_app(app, db)  # 👈 ADD THIS

    # Import blueprints
    from app.views import main, login, dashboard
    app.register_blueprint(main)
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    return app
