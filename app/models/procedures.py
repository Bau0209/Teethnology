from app import db

class Procedures(db.Model):
    __tablename__ = 'procedure_history'

    procedure_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.patient_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    procedure_date = db.Column(db.Date, nullable=False)
    treatment_procedure = db.Column(db.String(255), nullable=False)
    tooth_area = db.Column(db.String(10), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    treatment_plan = db.Column(db.Text)
    fee = db.Column(db.Integer, nullable=False)
    procedure_status = db.Column(db.String(255))
    notes = db.Column(db.Text)

    # Relationship (optional, to access patient details from a procedure)
    patient = db.relationship('PatientsInfo', backref=db.backref('procedures', lazy=True, cascade="all, delete-orphan"))
