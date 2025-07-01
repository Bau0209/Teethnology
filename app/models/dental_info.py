from app import db

class DentalInfo(db.Model):
    __tablename__ = 'dental_record'

    dental_record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.patient_id'), nullable=False)
    dental_record_image_link = db.Column(db.Text, nullable=False)
    periodontal_screening = db.Column(db.Text)
    occlusion = db.Column(db.Text)
    appliances = db.Column(db.Text)
    TMD = db.Column(db.Text)

    # Optional: define relationship to Patient model if needed
    patient = db.relationship('PatientsInfo', backref=db.backref('dental_record', lazy=True, cascade="all, delete-orphan"))
