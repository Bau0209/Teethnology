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

        for bracket, (min_age, max_age) in brackets.items():
            if min_age <= age <= max_age:
                results[bracket][appointment.appointment_type] += 1
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


def get_report_data(selected_year, current_month):
    """Build full report dictionary for frontend use."""
    services = get_services()
    monthly_appointment = get_monthly_appointment_count(selected_year)
    patient_month_data = get_monthly_new_and_returning_data(selected_year)
    new_returning_datasets = prepare_new_vs_returning_datasets(patient_month_data)

    # Assuming months is defined globally or elsewhere
    return {
        'months': months,  # Make sure 'months' is defined elsewhere
        'services': services,
        'monthly_appointments': monthly_appointment,
        'monthly_new_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='0'),
        'monthly_returning_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='1'),
        'new_returning_datasets': new_returning_datasets,
        'forecast_values': moving_average_forecast(monthly_appointment, window=5),
        'popular_services_by_age_bracket': process_popular_services_by_age(get_popular_services_by_age_bracket())
    }