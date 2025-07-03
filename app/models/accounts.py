from app import db

class Account(db.Model):
    __tablename__ = 'accounts'
    
    account_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    account_password = db.Column(db.String(255), nullable=False)
    access_level = db.Column(db.Enum('owner', 'staff'), default='staff', nullable=False)
    account_status = db.Column(db.Enum('active', 'inactive'), default='active', nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)