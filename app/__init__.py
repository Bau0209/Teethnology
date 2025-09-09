from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os
from datetime import timedelta

db = SQLAlchemy()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.permanent_session_lifetime = timedelta(minutes=15)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/branches'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB

    db.init_app(app)

    # Import and register blueprints
    from app.views import main, login, dashboard
    app.register_blueprint(main)
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    return app
