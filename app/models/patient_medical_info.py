from app import db

class PatientMedicalInfo(db.Model):
    __tablename__ = 'patient_medical_info'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.patient_id'), primary_key=True)
    medical_info_image_link = db.Column(db.Text)
    physician_name = db.Column(db.String(255))
    physician_specialty = db.Column(db.String(255))
    physician_office_address = db.Column(db.Text)
    physician_office_number = db.Column(db.String(15))
    in_good_health = db.Column(db.Boolean)
    medical_treatment_currently_undergoing = db.Column(db.Text)
    recent_illness_or_surgical_operation = db.Column(db.Text)
    when_illness_or_operation = db.Column(db.Text)
    when_why_hospitalized = db.Column(db.Text)
    medications_currently_taking = db.Column(db.Text)
    using_tabacco = db.Column(db.Boolean)
    using_alcohol_cocaine_drugs = db.Column(db.Boolean)
    allergies = db.Column(db.Text) #seperated by comma (,)
    bleeding_time = db.Column(db.String(20))
    is_pregnant = db.Column(db.Boolean)
    is_nursing = db.Column(db.Boolean)
    on_birth_control = db.Column(db.Boolean)
    blood_type = db.Column(db.String(20))
    blood_pressure = db.Column(db.String(20))
    illness_checklist = db.Column(db.Text) #seperated by comma (,)
    