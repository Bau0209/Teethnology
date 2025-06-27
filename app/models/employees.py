from app import db
from datetime import date

class Employee(db.Model):
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    employment_status = db.Column(db.Enum('active', 'inactive'), nullable=False)
    date_hired = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50))
    license_number = db.Column(db.String(255))
    shift_days = db.Column(db.String(255), nullable=False)
    shift_hours = db.Column(db.String(255), nullable=False)
    
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    branch = db.relationship('Branch', backref='employees', lazy=True)
    
    @property
    def full_name(self):
        #Combine first, middle(if any), and last name
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts)
    
    @property
    def age(self):
        today = date.today()
        if self.birthdate:
            return today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        return None
        