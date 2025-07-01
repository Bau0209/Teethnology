from app import db
from datetime import date

class PatientDentalInfo(db.Model):
    __tablename__ = 'dental_record'

    dental_record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    dental_record_image_link = db.Column(db.Text, nullable=False)
    periodontal_screening = db.Column(db.Text)
    occlusion = db.Column(db.Text)
    appliances = db.Column(db.Text)
    TMD = db.Column(db.Text)
    date_taken = db.Column(db.Date, default=date.today)

    # Optional: define relationship to Patient model if needed
    patient = db.relationship('Patient', backref='dental_records')
