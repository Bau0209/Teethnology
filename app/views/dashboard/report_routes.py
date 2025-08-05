from flask import render_template, request
from datetime import datetime, date
from sqlalchemy import extract, func
from collections import defaultdict

from app.views.dashboard import dashboard
from app.models import Transactions, Procedures
from app import db
from .report_datas import (
    get_today_revenue,
    get_monthly_revenue,
    get_appointments_count,
    moving_average_forecast
)

@dashboard.route('/reports')    
def reports():
    # Get current and last month dates
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    selected_year = request.args.get('year', type=int) or current_year
    
    monthly_revenue = get_monthly_revenue(selected_year)
    today_revenue = get_today_revenue()
    current_month_revenue = monthly_revenue[current_month - 1]
    forecast_values = moving_average_forecast(monthly_revenue, window=5)

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    appointments_this_month = get_appointments_count(current_month)

    # Top earning services
    service_month_data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        Procedures.treatment_procedure,
        func.sum(Transactions.total_amount_paid).label('total')
    ).join(Procedures, Procedures.procedure_id == Transactions.procedure_id)\
    .filter(extract('year', Transactions.transaction_datetime) == selected_year)\
    .group_by('month', Procedures.treatment_procedure)\
    .order_by('month')\
    .all()

    # Example: {'Cleaning': [1000, 1500, 0, ..., 2000], 'Whitening': [...], ...}
    service_monthly_totals = defaultdict(lambda: [0]*12)

    for month, service, total in service_month_data:
        service_monthly_totals[service][int(month) - 1] = float(total)

    # Convert to chart.js dataset format
    stacked_datasets = [{
        'label': service,
        'data': totals
    } for service, totals in service_monthly_totals.items()]

    # Color generator (optional)
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1',
            '#17a2b8', '#6610f2', '#fd7e14', '#20c997', '#6c757d']

    for i, ds in enumerate(stacked_datasets):
        ds['backgroundColor'] = colors[i % len(colors)]

    # --- BUSINESS INSIGHT BASED ONLY ON CURRENT DATA ---
    insight_lines = []

    # Insight 1: Appointment count
    appointment_insight = ["<strong>Appointments:</strong>"]
    if appointments_this_month < 10:
        appointment_insight.append("Appointment volume is low. Consider sending reminders or running promotions.")
    elif appointments_this_month < 20:
        appointment_insight.append("Appointment count is moderate. You may benefit from increased engagement.")
    else:
        appointment_insight.append("Great job! You have a healthy number of appointments this month.")
    insight_lines.append("<br>".join(appointment_insight))

    # Insight 2: Revenue performance
    revenue_insight = ["<strong>Revenues:</strong>"]
    if current_month_revenue < 10000:
        revenue_insight.append("Revenue is below ₱10,000. Review pricing or promote top services.")
    elif current_month_revenue < 20000:
        revenue_insight.append("Revenue is fair. Highlight best-sellers to boost earnings.")
    else:
        revenue_insight.append("Strong revenue this month! Keep up the momentum.")
    insight_lines.append("<br>".join(revenue_insight))

    # Insight 3: Top services
    # Filter to current month only
    current_month_services = [
        entry for entry in service_month_data if int(entry.month) == current_month
    ]

    # Find the top earning service this month
    top_service_this_month = None
    if current_month_services:
        top_service_this_month = max(current_month_services, key=lambda x: x.total)

    service_insight = ["<strong>Services:</strong>"]
    if top_service_this_month:
        service_insight.append(
            f"Top earning service this month: {top_service_this_month.treatment_procedure}. Consider upselling related procedures."
        )
    else:
        service_insight.append("No services recorded yet this month.")
    insight_lines.append("<br>".join(service_insight))

    insight_text = "<br><br>".join(insight_lines)

    return render_template('/dashboard/reports.html',
                           labels=months,
                           today_revenue=today_revenue,
                           values=monthly_revenue,
                           total_revenue=sum(monthly_revenue),
                           forecast_values=forecast_values,
                           current_month_revenue=current_month_revenue,
                           selected_year=selected_year,
                           current_year=current_year,
                           appointments_count=appointments_this_month,
                           stacked_datasets=stacked_datasets,
                           insight_text=insight_text)

@dashboard.route('/report_patients') 
def report_patients():
   return render_template('/dashboard/report_patient.html', current_year=datetime.now().year)

@dashboard.route('/report_marketing')    
def report_marketing():
    return render_template('/dashboard/report_marketing.html', current_year=datetime.now().year)

@dashboard.route('/report_inventory') 
def report_inventory():
    return render_template('/dashboard/report_inventory.html', current_year=datetime.now().year)


