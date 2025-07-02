from app import db

class Procedures(db.Model):
    __tablename__ = 'procedure_history'

    procedure_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.patient_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    # NEW: Appointment relationship
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)

    procedure_date = db.Column(db.Date, nullable=False)
    treatment_procedure = db.Column(db.String(255), nullable=False)
    tooth_area = db.Column(db.String(10), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    treatment_plan = db.Column(db.Text)
    fee = db.Column(db.Integer, nullable=False)
    procedure_status = db.Column(db.String(255))
    notes = db.Column(db.Text)

    # Relationships
    patient = db.relationship('PatientsInfo', backref=db.backref('procedures', lazy=True, cascade="all, delete-orphan"))
    appointment = db.relationship('Appointments', backref=db.backref('procedures', lazy=True))
