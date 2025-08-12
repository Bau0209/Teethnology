from datetime import datetime
from app import db
import json
from app.models import Appointments, Branch, PatientsInfo, Archive

def archive_and_delete(record_id, table_name, user):
    try:
        # Map table names to models
        model_map = {
            'patients': PatientsInfo,
            'branches': Branch,
            'appointments': Appointments
        }

        if table_name not in model_map:
            return False, 'Unsupported table'

        model = model_map[table_name]
        record = model.query.get(record_id)

        if not record:
            return False, 'Record not found'

        if not hasattr(record, 'as_dict'):
            return False, f"{table_name} model missing as_dict() method"

        # Archive the main record
        archive_record = Archive(
            original_id=record.id,
            table_name=table_name,
            archived_data=json.dumps(record.as_dict()),  # Store as JSON string
            archived_by=user,
            archived_at=datetime.utcnow()
        )
        db.session.add(archive_record)

        # Special handling for patients → also archive their appointments
        if table_name == 'patients':
            appointments = Appointments.query.filter_by(patient_id=record.id).all()
            for appt in appointments:
                db.session.add(Archive(
                    original_id=appt.id,
                    table_name='appointments',
                    archived_data=json.dumps(appt.as_dict()),
                    archived_by=user,
                    archived_at=datetime.utcnow()
                ))
                db.session.delete(appt)

        # Delete the main record
        db.session.delete(record)
        db.session.commit()

        return True, 'Record archived and deleted successfully'

    except Exception as e:
        db.session.rollback()
        return False, str(e)

