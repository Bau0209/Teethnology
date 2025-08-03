from flask import jsonify, request
from datetime import datetime
from app import db
import json
from app.models import Appointments, Branch, Transactions, PatientsInfo, Archive

def archive_and_delete(record_id, table_name, user):
    """
    Permanently removes a record and stores it in archive table
    :param record_id: ID of record to remove
    :param table_name: Name of source table
    :param user: User performing the action
    :return: Tuple (success, message)
    """
    try:
        # 1. Get the original record
        if table_name == 'appointments':
            record = Appointments.query.get(record_id)
        elif table_name == 'patients':
            record = PatientsInfo.query.get(record_id)
        else:
            return False, "Invalid table name"
        
        if not record:
            return False, "Record not found"
        
        # 2. Convert to JSON-serializable dictionary
        record_data = {column.name: getattr(record, column.name) 
                      for column in record.__table__.columns}
        
        # Handle datetime objects
        for key, value in record_data.items():
            if hasattr(value, 'isoformat'):  # Handles date/datetime
                record_data[key] = value.isoformat()
        
        # 3. Create archive record
        archived_record = Archive(
            original_id=record_id,
            table_name=table_name,
            data=json.dumps(record_data),
            archived_by=user
        )
        
        db.session.add(archived_record)
        
        # 4. Delete original record
        db.session.delete(record)
        db.session.commit()
        
        return True, "Record archived successfully"
    
    except Exception as e:
        db.session.rollback()
        return False, f"Error archiving record: {str(e)}"