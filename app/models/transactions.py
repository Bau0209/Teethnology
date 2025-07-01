from app import db
from datetime import datetime

class Transactions(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure_history.procedure_id'), nullable=False)

    receipt_number = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.Enum('Cash', 'Card', 'GCash', 'Maya', 'Insurance', 'Other'), nullable=False)
    transaction_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dentist_name = db.Column(db.String(255), nullable=False)
    service_detail = db.Column(db.Text, nullable=False)
    total_amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_image_link = db.Column(db.Text)

    # Relationships
    procedure = db.relationship('Procedures', backref=db.backref('transactions', lazy=True))