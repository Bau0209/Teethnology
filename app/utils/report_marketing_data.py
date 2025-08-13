from app import db
from sqlalchemy import func, extract
from collections import defaultdict
from datetime import datetime

from app.models import Appointments, PatientsInfo

# Make sure 'months' is defined here or imported
months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

def get_appointments_count(month):
    return db.session.query(func.count(Appointments.appointment_id))\
        .filter(extract('month', Appointments.appointment_date) == month)\
        .scalar()

def get_monthly_new_or_returning_patients(selected_year, is_returning):
    """
    Returns a list of appointment counts for either new or returning patients per month.
    - is_returning = 0 → New patients
    - is_returning = 1 → Returning patients
    Output format: [Jan, Feb, ..., Dec] (12 integers)
    Useful for single-series charts showing only one patient type at a time.
    """
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

def get_monthly_new_and_returning_data(selected_year):
    """
    Returns combined monthly appointment counts for both new and returning patients.
    Output format: List of tuples → [(month, returning_flag, count), ...]
    Example: [(1, 0, 12), (1, 1, 18), (2, 0, 10), ...]
    Useful for grouped or stacked charts comparing new vs returning patients side-by-side.
    Optimized for preparing multi-series datasets.
    """
    new_data = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        Appointments.returning_patient,
        func.count(Appointments.appointment_id).label('count')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year,
        Appointments.returning_patient == 0
    ).group_by('month', Appointments.returning_patient).all()

    returning_data = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        Appointments.returning_patient,
        func.count(Appointments.appointment_id).label('count')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year,
        Appointments.returning_patient == 1
    ).group_by('month', Appointments.returning_patient).all()

    combined = []
    for row in new_data + returning_data:
        combined.append((int(row.month), int(row.returning_patient), int(row.count)))
    
    return combined
def get_popular_services_by_age_bracket():
    """Count popular services grouped by age brackets."""
    brackets = {
        '0-12': (0, 12),
        '13-19': (13, 19),
        '20-35': (20, 35),
        '36-50': (36, 50),
        '51+': (51, 150)
    }

    results = {bracket: defaultdict(int) for bracket in brackets}

    appointments = db.session.query(Appointments, PatientsInfo).join(
        PatientsInfo, Appointments.patient_id == PatientsInfo.patient_id
    ).all()

    today = datetime.today()

    for appointment, patient in appointments:
        if not patient.birthdate:
            continue

        age = today.year - patient.birthdate.year - (
            (today.month, today.day) < (patient.birthdate.month, patient.birthdate.day)
        )

        # Ensure appointment type is always a string
        appt_type = getattr(appointment, 'appointment_type', None)
        if not appt_type:  
            appt_type = "Unknown"

        for bracket, (min_age, max_age) in brackets.items():
            if min_age <= age <= max_age:
                results[bracket][appt_type] += 1
                break

    # Convert to {bracket: [(service, count), ...]}
    return {
        bracket: sorted(services.items(), key=lambda x: x[1], reverse=True)
        for bracket, services in results.items()
    }


def process_popular_services_by_age(raw_data):
    """Format service data for Chart.js stacked bar input."""
    all_services = set()
    for service_list in raw_data.values():
        for service, _ in service_list:
            all_services.add(service)

    all_services = sorted(all_services)

    datasets = []
    for age_group, service_data in raw_data.items():
        service_counts = {service: count for service, count in service_data}
        data = [service_counts.get(service, 0) for service in all_services]
        datasets.append({
            'label': age_group,
            'data': data
        })

    return {
        'labels': all_services,
        'datasets': datasets
    }


def get_popular_services_by_gender():
    """Count popular services grouped by gender."""
    results = defaultdict(lambda: defaultdict(int))

    appointments = db.session.query(Appointments, PatientsInfo).join(
        PatientsInfo, Appointments.patient_id == PatientsInfo.patient_id
    ).all()

    for appointment, patient in appointments:
        # Use 'sex' from the model instead of 'gender'
        gender = (patient.sex.strip().capitalize()
                  if getattr(patient, 'sex', None)
                  else "Unknown")
        results[gender][appointment.appointment_type] += 1

    # Convert results to sorted lists
    return {
        gender: sorted(services.items(), key=lambda x: x[1], reverse=True)
        for gender, services in results.items()
    }


def get_services():
    """Fetch distinct appointment types from the appointments table."""
    appointment_types = db.session.query(Appointments.appointment_type).distinct().all()
    return [atype[0] for atype in appointment_types if atype[0]]

def get_report_data(selected_year, current_month):
    """Build full report dictionary for frontend use."""
    services = get_services()
    popular_by_age= get_popular_services_by_age_bracket()
    popular_by_gender= get_popular_services_by_gender()

    return {
        'months': months,  # Make sure 'months' is defined elsewhere
        'services': services,
        'popular_services_by_age_bracket': process_popular_services_by_age(get_popular_services_by_age_bracket()),
        'popular_services_by_gender': process_popular_services_by_age(get_popular_services_by_gender())
    }
