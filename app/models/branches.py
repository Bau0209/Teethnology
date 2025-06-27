from app import db

class Branch(db.Model):
    __tablename__ = 'branch'
    
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    full_address = db.Column(db.String(255), nullable=False)
    clinic_description = db.Column(db.Text, nullable=False)
    chief_dentist = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    clinic_open_hour = db.Column(db.Time, nullable=False)
    clinic_close_hour = db.Column(db.Time, nullable=False)
    services = db.Column(db.Text, nullable=False)
    
class ClinicBranchImage(db.Model):
    __tablename__ = 'clinic_branch_images'

    image_id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.Text, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
