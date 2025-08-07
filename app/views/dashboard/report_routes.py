from flask import render_template, request
from datetime import datetime, date
from sqlalchemy import extract, func
from collections import defaultdict

from app.views.dashboard import dashboard
from app.models import Transactions, Procedures
from app import db
from ...utils.report_revenue_datas import (
    get_report_data as get_revenue_data, 
    generate_insights as generate_revenue_insights
)
from ...utils.report_patients_datas import (
    get_report_data as get_patients_data
)

@dashboard.route('/reports')    
def reports():
    today = datetime.now()
    current_month = today.month
    selected_year = request.args.get('report_revenue_selected_year', type=int) or today.year
    revenue_data = get_revenue_data(selected_year, current_month)
    revenue_insights = generate_revenue_insights(revenue_data)
    patients_data = get_patients_data(selected_year, current_month)

    return render_template('/dashboard/reports.html',
                           labels=revenue_data['months'],
                           today_revenue=revenue_data['today_revenue'],
                           values=revenue_data['monthly_revenue'],
                           total_revenue=sum(revenue_data['monthly_revenue']),
                           forecast_values=revenue_data['forecast_values'],
                           current_month_revenue=revenue_data['current_month_revenue'],
                           selected_year=selected_year,
                           current_year=today.year,
                           appointments_count=patients_data['monthly_appointments'][current_month - 1],
                           stacked_datasets=revenue_data['stacked_datasets'],
                           insight_text=revenue_insights)

@dashboard.route('/report_patients') 
def report_patients():
    today = datetime.now()
    current_month = today.month
    selected_year = request.args.get('report_revenue_selected_year', type=int) or today.year
    patients_data = get_patients_data(selected_year, current_month)
    
    return render_template('/dashboard/report_patient.html',
                           current_year=today.year,
                           selected_year=selected_year,
                           current_month_new_patient = patients_data['monthly_new_patients'][current_month - 1],
                           current_month_returning_patient = patients_data['monthly_returning_patients'][current_month - 1],
                           current_month_appointment=patients_data['monthly_appointments'][current_month - 1])
                        

@dashboard.route('/report_marketing')    
def report_marketing():
    return render_template('/dashboard/report_marketing.html', current_year=datetime.today().year)

@dashboard.route('/report_inventory') 
def report_inventory():
    return render_template('/dashboard/report_inventory.html', current_year=datetime.today().year)


