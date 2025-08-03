from app import db
from datetime import datetime

class Archive(db.Model):
    __tablename__ = 'archive'
    
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    archived_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived_by = db.Column(db.String(100))