from app import db
from datetime import date

class PatientsInfo(db.Model):
    __tablename__ = 'patient_info'
    
    patient_id = db.Column(db.Integer, primary_key=True )
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    baranggay = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    initial_consultation_reason = db.Column(db.Text, nullable=False)
    occupation = db.Column(db.String(255))
    office_number = db.Column(db.String(255))
    guardian_first_name = db.Column(db.String(255))
    guardian_middle_name = db.Column(db.String(255))
    guardian_last_name = db.Column(db.String(255))
    guardian_occupation = db.Column(db.String(255))
    reffered_by = db.Column(db.String(255))
    previous_dentist = db.Column(db.String(255))
    last_dental_visit = db.Column(db.Date)
    image_link = db.Column(db.Text)
    
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'))
    branch = db.relationship('Branch', backref='patients', lazy=True)
    
    @property
    def patient_full_name(self):
        #Combine the first, middle (if any), and last name
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        
        return ' '.join(parts)
    
    @property
    def guardian_full_name(self):
        parts = [self.guardian_first_name, self.guardian_middle_name, self.guardian_last_name]
        return ' '.join(filter(None, parts))
    
    @property
    def age(self):
        today = date.today()
        if self.birthdate:
            return today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        
        return None