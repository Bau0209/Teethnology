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

def get_monthly_new_and_returning_data(selected_year, selected_branch):
    """
    Returns combined monthly appointment counts for both new and returning patients.
    Output format: List of tuples → [(month, returning_flag, count), ...]
    Example: [(1, 0, 12), (1, 1, 18), (2, 0, 10), ...]
    Useful for grouped or stacked charts comparing new vs returning patients side-by-side.
    """

    # Base query for new patients
    new_query = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        Appointments.returning_patient,
        func.count(Appointments.appointment_id).label('count')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year,
        Appointments.returning_patient == 0
    )

    # Base query for returning patients
    returning_query = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        Appointments.returning_patient,
        func.count(Appointments.appointment_id).label('count')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year,
        Appointments.returning_patient == 1
    )

    # Apply branch filter if not "all"
    if selected_branch != 'all':
        branch_id = int(selected_branch)
        new_query = new_query.filter(Appointments.branch_id == branch_id)
        returning_query = returning_query.filter(Appointments.branch_id == branch_id)

    # Execute queries
    new_data = new_query.group_by('month', Appointments.returning_patient).all()
    returning_data = returning_query.group_by('month', Appointments.returning_patient).all()

    # Combine results
    combined = []
    for row in new_data + returning_data:
        combined.append((int(row.month), int(row.returning_patient), int(row.count)))

    return combined

def get_monthly_appointment_count(selected_year, selected_branch):
    query = db.session.query(
        extract('month', Appointments.appointment_date).label('month'),
        func.count(Appointments.patient_id).label('total')
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year
    )

    # Filter by branch_id if not "all"
    if selected_branch != 'all':
        query = query.filter(Appointments.branch_id == int(selected_branch))

    data = query.group_by('month').order_by('month').all()

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

def get_new_vs_returning_by_age_bracket(selected_year, selected_branch):
    """Count new vs returning patients grouped by age brackets for a specific year."""
    brackets = {
        '0-17': (0, 17),
        '18-30': (18, 30),
        '31-59': (31, 59),
        '60+': (60, 150)
    }

    results = {bracket: {'New Patients': 0, 'Returning Patients': 0} for bracket in brackets}

    # Base query: Appointments + PatientsInfo
    query = db.session.query(Appointments, PatientsInfo).join(
        PatientsInfo, Appointments.patient_id == PatientsInfo.patient_id
    ).filter(
        extract('year', Appointments.appointment_date) == selected_year
    )

    # Apply branch filter if not "all"
    if selected_branch != 'all':
        query = query.filter(Appointments.branch_id == int(selected_branch))

    appointments = query.all()
    today = datetime.today()

    # Process results
    for appointment, patient in appointments:
        if not patient.birthdate:
            continue

        # Calculate age
        age = today.year - patient.birthdate.year - (
            (today.month, today.day) < (patient.birthdate.month, patient.birthdate.day)
        )

        # Assign to age bracket
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

def prepare_forecast_datasets(actual_values, forecast_values):
    """Prepare dataset for actual vs forecast comparison chart."""
    return {
        'labels': months,
        'datasets': [
            {
                'label': 'Actual Appointments',
                'data': actual_values,
                'borderColor': '#3e95cd',
                'backgroundColor': 'rgba(62, 149, 205, 0.2)',
                'fill': False,
                'borderWidth': 2
            },
            {
                'label': 'Forecasted Appointments',
                'data': forecast_values,
                'borderColor': '#ff6384',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderWidth': 2,
                'borderDash': [5, 5],
                'fill': False
            }
        ]
    }

def get_report_data(selected_year, selected_branch):
    services = get_services()
    monthly_appointment = get_monthly_appointment_count(selected_year, selected_branch)
    patient_month_data = get_monthly_new_and_returning_data(selected_year, selected_branch)
    new_returning_datasets = prepare_new_vs_returning_datasets(patient_month_data)
    forecast_values = moving_average_forecast(monthly_appointment, window=5)

    return { 
        'months': months,
        'services': services,
        'monthly_appointments': monthly_appointment,
        'monthly_new_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='0'),
        'monthly_returning_patients': get_monthly_new_or_returning_patients(selected_year, is_returning='1'),
        'new_returning_datasets': new_returning_datasets,
        'forecast_values': forecast_values,
        'forecast_chart_data': prepare_forecast_datasets(monthly_appointment, forecast_values),
        'new_vs_returning_by_age': process_new_vs_returning_by_age(
            get_new_vs_returning_by_age_bracket(selected_year, selected_branch)
        )
    }

def generate_patient_insights(data):
    current_month = datetime.now().month
    insights = []

    # --- Calculate averages ---
    monthly_appts = data['monthly_appointments']
    valid_appts = [v for v in monthly_appts if v > 0]
    avg_appts = sum(valid_appts) / max(1, len(valid_appts))

    forecast_vals = data['forecast_values']
    valid_forecast = [v for v in forecast_vals if v > 0]
    avg_forecast = sum(valid_forecast) / max(1, len(valid_forecast))

    # --- Current Appointments ---
    current_appointments = monthly_appts[current_month - 1]
    if current_appointments < avg_appts * 0.9:
        current_msg = f"Current appointments are significantly below our historical average."
    elif current_appointments > avg_appts * 1.1:
        current_msg = f"Current appointments are trending well above our historical average."
    else:
        current_msg = f"Current appointment volume is consistent with our historical average."
    insights.append(f"<strong>Appointments (Current Month):</strong><br>{current_msg}")

    # --- Forecast Appointments (Next Month) ---
    forecast_next = forecast_vals[current_month - 1]
    if forecast_next < avg_forecast * 0.9:
        forecast_msg = f"Next month's forecast indicates a potential decline in patient demand."
    elif forecast_next > avg_forecast * 1.1:
        forecast_msg = f"Next month's forecast projects strong growth in patient demand."
    else:
        forecast_msg = f"Next month's forecast aligns with typical patient volume expectations."
    insights.append(f"<strong>Appointments (Forecast):</strong><br>{forecast_msg}")

    # --- New vs Returning Patients ---
    new_patients = data['monthly_new_patients'][current_month - 1]
    returning_patients = data['monthly_returning_patients'][current_month - 1]

    if new_patients > returning_patients:
        patient_mix_msg = f"Patient acquisition efforts are successfully expanding our client base."
    elif returning_patients > new_patients:
        patient_mix_msg = f"Patient retention rates demonstrate strong loyalty and satisfaction."
    else:
        patient_mix_msg = f"We're maintaining a healthy balance between new and returning patients."
    insights.append(f"<strong>New vs Returning:</strong><br>{patient_mix_msg}")

    # --- Recommendation & Feedback ---
    reco_msg = ["<strong>Recommendation:</strong>"]

    # Based on Current + Forecast Appointments
    if current_appointments < avg_appts and forecast_next < avg_forecast:
        reco_msg.append(
            "Increase visibility through marketing campaigns and reactivation of past patients.<br>"
        )
    elif current_appointments < avg_appts and forecast_next >= avg_forecast:
        reco_msg.append(
            "Boost awareness campaigns to capture the expected upswing next month.<br>"
        )
    elif current_appointments >= avg_appts and forecast_next < avg_forecast:
        reco_msg.append(
            "Secure patient loyalty and follow-ups to offset a potential dip.<br>"
        )
    else:
        reco_msg.append(
            "Maintain consistent outreach and patient engagement programs. <br>"
        )

    # Based on New vs Returning Patients
    if new_patients > returning_patients:
        reco_msg.append(
            "Additionally: Focus on converting new patients into repeat visits."
        )
    elif returning_patients > new_patients:
        reco_msg.append(
            "Additionally: Strengthen new patient acquisition campaigns."
        )
    else:
        reco_msg.append(
            "Additionally: Balance acquisition and retention efforts."
        )

    insights.append("<br>".join(reco_msg))

    return "<br><br>".join(insights)