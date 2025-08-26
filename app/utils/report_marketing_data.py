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
        '0-17': (0, 17),
        '18-30': (19, 30),
        '31-59': (31, 59),
        '60+': (60, 150)
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
        appt_type = getattr(appointment, 'appointment_category', None)
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
        results[gender][appointment.appointment_category] += 1

    # Convert results to sorted lists
    return {
        gender: sorted(services.items(), key=lambda x: x[1], reverse=True)
        for gender, services in results.items()
    }


def get_services():
    """Fetch distinct appointment types from the appointments table."""
    appointment_categories = db.session.query(Appointments.appointment_category).distinct().all()
    return [atype[0] for atype in appointment_categories if atype[0]]

def get_report_data(selected_year, current_month):
    """Build full report dictionary for frontend use."""
    services = get_services()
    popular_by_age= get_popular_services_by_age_bracket()
    popular_by_gender= get_popular_services_by_gender()

    return {
        'months': months, 
        'services': services,
        'popular_services_by_age_bracket': process_popular_services_by_age(get_popular_services_by_age_bracket()),
        'popular_services_by_gender': process_popular_services_by_age(get_popular_services_by_gender())
    }
def generate_marketing_insights(data, current_month):
    insights = []

    # --- Historical averages ---
    monthly_counts = [get_appointments_count(m) for m in range(1, 13)]
    valid_counts = [v for v in monthly_counts if v > 0]
    avg_appts = sum(valid_counts) / max(1, len(valid_counts))

    # --- Current appointments ---
    current_appts = get_appointments_count(current_month)

    if current_appts < avg_appts * 0.9:
        current_msg = f"Current appointment volume is underperforming against historical trends."
    elif current_appts > avg_appts * 1.1:
        current_msg = f"Current appointment volume is exceeding historical performance benchmarks."
    else:
        current_msg = f"Current appointment volume is consistent with historical performance."
    insights.append(f"<strong>Appointments:</strong><br>{current_msg}")

    # --- Forecast using 3-month moving average ---
    past_months = [get_appointments_count(m) for m in range(max(1, current_month - 2), current_month + 1)]
    forecast_next = round(sum(past_months) / max(1, len(past_months)), 2)

    if forecast_next < avg_appts * 0.9:
        forecast_msg = f"Marketing forecasts indicate a potential decline in future patient demand."
    elif forecast_next > avg_appts * 1.1:
        forecast_msg = f"Marketing forecasts project strong growth in upcoming patient demand."
    else:
        forecast_msg = f"Marketing forecasts suggest stable patient demand in the coming month."
    insights.append(f"<strong>Forecast:</strong><br>{forecast_msg}")

    # --- Recommendation + Feedback (Decision Tree) ---
    reco_msg = ["<strong>Recommendation:</strong>"]

    if current_appts < avg_appts * 0.9 and forecast_next < avg_appts * 0.9:
        reco_msg.append(
            "Boost marketing campaigns immediately (ads, promos, partnerships)."
        )
    elif current_appts < avg_appts * 0.9 and forecast_next > avg_appts * 1.1:
        reco_msg.append(
            "Prepare to capture upcoming demand surge by scaling campaigns and resources."
        )
    elif current_appts > avg_appts * 1.1 and forecast_next < avg_appts * 0.9:
        reco_msg.append(
            "Focus on retention and loyalty programs to balance the expected slowdown."
        )
    elif current_appts > avg_appts * 1.1 and forecast_next > avg_appts * 1.1:
        reco_msg.append(
            "Maintain momentum and consider scaling staff/resources to support growth."
        )
    else:
        reco_msg.append(
            "Maintain current marketing strategies, but monitor trends closely."
        )

    insights.append("<br>".join(reco_msg))

    return "<br><br>".join(insights)


