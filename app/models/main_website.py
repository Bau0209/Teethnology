from app import db

class MainWeb(db.Model):
    __tablename__ = 'main_website'

    main_website = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(255), nullable=False)
    about_us = db.Column(db.Text, nullable=False)
    services = db.Column(db.Text, nullable=False)  # comma-separated
    main_email = db.Column(db.String(100), nullable=False)
    main_contact_number = db.Column(db.String(20), nullable=False)
