from app import db
from sqlalchemy import func, extract

from app.models import Appointments

def get_appointments_count(month):
    return db.session.query(func.count(Appointments.appointment_id))\
        .filter(extract('month', Appointments.appointment_date) == month)\
        .scalar()

def get_monthly_new_or_returning_patients(selected_year, is_returning):
    data = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        func.count(Appointments.appointment_id).label('total')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year,
        Appointments.returning_patient == is_returning
    ).group_by('month').order_by('month').all()

    values = [0] * 12
    for month, total in data:
        values[int(month) - 1] = int(total)

    return values

def get_monthly_appointment_count(selected_year):
    data = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        func.count(Appointments.patient_id).label('total')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year
    ).group_by('month').order_by('month').all()
    
    values = [0] * 12
    for month, total in data:
        values[int(month) - 1] = int(total)
        
    return values
    
def get_report_data(selected_year, current_month):
    
    return {
        'monthly_appointments': get_monthly_appointment_count(selected_year),
        'monthly_new_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='0'),
        'monthly_returning_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='1')         
    }