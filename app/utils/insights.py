from datetime import datetime
from sqlalchemy import func, extract
from app.models import Transactions, Procedures, Appointments
from app import db

def generate_business_insight():
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1

    revenue_data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        func.sum(Transactions.total_amount_paid).label('total')
    ).group_by(extract('month', Transactions.transaction_datetime))\
     .order_by(extract('month', Transactions.transaction_datetime)).all()

    values = [0] * 12
    for month, total in revenue_data:
        values[int(month) - 1] = float(total)

    current_revenue = values[current_month - 1]
    last_revenue = values[last_month - 1]
    growth_rate = ((current_revenue - last_revenue) / last_revenue * 100) if last_revenue > 0 else 0

    appointments_this_month = db.session.query(func.count(Appointments.appointment_id))\
        .filter(extract('month', Appointments.appointment_date) == current_month)\
        .filter(extract('year', Appointments.appointment_date) == current_year)\
        .scalar()

    top_services = db.session.query(
        Appointments.appointment_type,
        func.sum(Transactions.total_amount_paid).label('revenue')
    ).join(
        Procedures, Procedures.appointment_id == Appointments.appointment_id
    ).join(
        Transactions, Transactions.procedure_id == Procedures.procedure_id
    ).group_by(
        Appointments.appointment_type
    ).order_by(
        func.sum(Transactions.total_amount_paid).desc()
    ).limit(5).all()

    top_service_labels = [s[0] for s in top_services]

    insight_lines = []

    # Insight 1: Appointments
    appointment_insight = ["<strong>Appointments:</strong>"]
    if appointments_this_month < 10:
        appointment_insight.append("Appointment volume is low. Consider sending reminders or running promotions.")
    elif appointments_this_month < 20:
        appointment_insight.append("Appointment count is moderate. You may benefit from increased engagement.")
    else:
        appointment_insight.append("Great job! You have a healthy number of appointments this month.")
    insight_lines.append("<br>".join(appointment_insight))

    # Insight 2: Revenue
    revenue_insight = ["<strong>Revenues:</strong>"]
    if current_revenue < 10000:
        revenue_insight.append("Revenue is below ₱10,000. Review pricing or promote top services.")
    elif current_revenue < 20000:
        revenue_insight.append("Revenue is fair. Highlight best-sellers to boost earnings.")
    else:
        revenue_insight.append("Strong revenue this month! Keep up the momentum.")
    insight_lines.append("<br>".join(revenue_insight))

    # Insight 3: Top service
    service_insight = ["<strong>Services:</strong>"]
    if top_service_labels:
        service_insight.append(f"Top earning service: {top_service_labels[0]}. Consider upselling related procedures.")
    insight_lines.append("<br>".join(service_insight))

    return "<br><br>".join(insight_lines)
