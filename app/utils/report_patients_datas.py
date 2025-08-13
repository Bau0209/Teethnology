from app import db
from sqlalchemy import func, extract
from collections import defaultdict
from datetime import datetime

from app.models import Appointments, PatientsInfo

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

def prepare_new_vs_returning_datasets(patient_month_data):
    grouped_data = {
        'New Patients': [0] * 12,
        'Returning Patients': [0] * 12
    }

    for month, returning_flag, count in patient_month_data:
        label = 'Returning Patients' if returning_flag else 'New Patients'
        grouped_data[label][month - 1] = count

    colors = ['#007bff', '#28a745']

    stacked_datasets = []
    for i, (label, totals) in enumerate(grouped_data.items()):
        stacked_datasets.append({
            'label': label,
            'data': totals,
            'backgroundColor': colors[i % len(colors)]
        })

    return stacked_datasets

def moving_average_forecast(values, window):
    """
    Forecast next 12 months using the average of the previous N months.
    If fewer than N months, fallback to average of available months.
    """
    forecast = []
    for i in range(len(values)):
        start = max(0, i - window)
        window_values = values[start:i]
        if window_values:
            forecast_value = sum(window_values) / len(window_values)
        else:
            forecast_value = values[i]  # or fallback average
        forecast.append(round(forecast_value, 2))
    return forecast

def get_services():
    """Fetch distinct appointment types from the appointments table."""
    appointment_types = db.session.query(Appointments.appointment_type).distinct().all()
    return [atype[0] for atype in appointment_types if atype[0]]


def get_new_vs_returning_by_age_bracket():
    """Count new vs returning patients grouped by age brackets."""
    brackets = {
        '0-12': (0, 12),
        '13-19': (13, 19),
        '20-35': (20, 35),
        '36-50': (36, 50),
        '51+': (51, 150)
    }

    results = {bracket: {'New Patients': 0, 'Returning Patients': 0} for bracket in brackets}

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

        for bracket, (min_age, max_age) in brackets.items():
            if min_age <= age <= max_age:
                label = 'Returning Patients' if appointment.returning_patient else 'New Patients'
                results[bracket][label] += 1
                break

    return results

def process_new_vs_returning_by_age(raw_data):
    """Format age-bracket patient data for Chart.js."""
    labels = list(raw_data.keys())  # Age groups as labels
    datasets = []

    # Extract data for each category
    for category, color in [('New Patients', "#ffae00"), ('Returning Patients', "#76a728")]:
        data = [raw_data[bracket][category] for bracket in labels]
        datasets.append({
            'label': category,
            'data': data,
            'backgroundColor': color
        })

    return {
        'labels': labels,
        'datasets': datasets
    }


def get_report_data(selected_year, current_month):
    services = get_services()
    monthly_appointment = get_monthly_appointment_count(selected_year)
    patient_month_data = get_monthly_new_and_returning_data(selected_year)
    new_returning_datasets = prepare_new_vs_returning_datasets(patient_month_data)

    return {
        'months': months,
        'services': services,
        'monthly_appointments': monthly_appointment,
        'monthly_new_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='0'),
        'monthly_returning_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='1'),
        'new_returning_datasets': new_returning_datasets,
        'forecast_values': moving_average_forecast(monthly_appointment, window=5),
        'new_vs_returning_by_age': process_new_vs_returning_by_age(
            get_new_vs_returning_by_age_bracket()
        )
    }
