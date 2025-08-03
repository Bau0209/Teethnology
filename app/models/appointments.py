from app import db
from datetime import datetime

class Appointments(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.patient_id'), nullable=False)

    appointment_sched = db.Column(db.DateTime, nullable=False)
    alternative_sched = db.Column(db.DateTime)

    appointment_type = db.Column(db.String(100), nullable=False)
    appointment_status = db.Column(db.Enum('pending', 'approved', 'cancelled'), nullable=False, default='pending')

    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime)
    approved_by = db.Column(db.String(255))

    returning_patient = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    procedures = db.relationship('Procedures', backref='appointments', lazy=True)
    branch = db.relationship('Branch', backref=db.backref('appointments', lazy=True))
    patient = db.relationship('PatientsInfo', backref=db.backref('appointments', lazy=True))

class ArchivedAppointments(db.Model):
    __tablename__ = 'archived_appointments'

    id = db.Column(db.Integer, primary_key=True)
    original_appointment_id = db.Column(db.Integer)
    patient_id = db.Column(db.Integer)
    appointment_sched = db.Column(db.DateTime)
    alternative_sched = db.Column(db.DateTime)
    appointment_type = db.Column(db.String(100))
    appointment_status = db.Column(db.String(50))
    request_date = db.Column(db.DateTime)
    rejection_date = db.Column(db.DateTime)
    rejected_by = db.Column(db.String(100))
    returning_patient = db.Column(db.String(10))
    archived_at = db.Column(db.DateTime, default=datetime.utcnow)
    cancelled_date = db.Column(db.DateTime)
    cancelled_by = db.Column(db.String(100))
