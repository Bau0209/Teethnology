from flask import jsonify, request
from datetime import datetime
from app import db
import json
from app.models import Appointments, Branch, Transactions, PatientsInfo, Archive

def archive_and_delete(record_id, table_name, user):
    try:
        if table_name == 'patients':
            record = PatientsInfo.query.get(record_id)
        elif table_name == 'branches':
            record = Branch.query.get(record_id)
        else:
            return False, 'Unsupported table'

        if not record:
            return False, 'Record not found'

        # Match Archive model's columns
        archive_record = Archive(
            original_id=record.id,
            table_name=table_name,
            data=json.dumps(record.as_dict()),  # Ensure as_dict() exists in model
            archived_by=user,
            archived_at=datetime.utcnow()
        )

        db.session.add(archive_record)
        db.session.delete(record)
        db.session.commit()
        return True, 'Record archived and deleted'
    
    except Exception as e:
        db.session.rollback()
        return False, str(e)
