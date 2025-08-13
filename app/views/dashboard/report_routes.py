from flask import render_template, request, g
from datetime import datetime
import subprocess

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

from ...utils.report_marketing_data import (
    get_report_data as get_marketing_data,
)
from ...utils.report_inventory_data import (
    get_inventory_report_data as get_inventory_data,
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
                           stacked_datasets=revenue_data['stacked_datasets'],
                           insight_text=revenue_insights)

@dashboard.route('/report_patients') 
def report_patients():
    today = datetime.now()
    current_month = today.month
    selected_year = request.args.get('report_revenue_selected_year', type=int) or today.year
    patients_data = get_patients_data(selected_year, current_month)
    
    return render_template('/dashboard/report_patient.html',
                           months_labels=patients_data['months'],
                           service_labels=patients_data['services'],
                           values=patients_data['monthly_appointments'],
                           new_returning_stacked_datasets=patients_data['new_returning_datasets'],
                           forecast_values=patients_data['forecast_values'],
                           new_vs_returning_by_age=patients_data['new_vs_returning_by_age'],  # updated key
                           current_year=today.year,
                           selected_year=selected_year,
                           current_month_new_patient=patients_data['monthly_new_patients'][current_month - 1],
                           current_month_returning_patient=patients_data['monthly_returning_patients'][current_month - 1],
                           current_month_appointment=patients_data['monthly_appointments'][current_month - 1])


@dashboard.route('/report_marketing')
def report_marketing():
    selected_year = datetime.today().year
    current_month = datetime.today().month
    report_data = get_marketing_data(selected_year, current_month)

    return render_template('/dashboard/report_marketing.html',
                            current_year=selected_year,
                            popular_service_by_age=report_data['popular_services_by_age_bracket'],
                            popular_service_by_gender=report_data['popular_services_by_gender'])


@dashboard.route('/report_inventory') 
def report_inventory():
    selected_branch = g.get('selected_branch', 'all')
    data = get_inventory_data(selected_branch)
    return render_template(
        'dashboard/report_inventory.html',
        low_stock=data['low_stock'],
        out_of_stock=data['out_of_stock'],
        expired=data['expired'],
        inventory_report_data=data,
        current_year=datetime.now().year,  
        selected_year=datetime.now().year
    )

