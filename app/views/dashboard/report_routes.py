from flask import render_template, request, g, jsonify
from datetime import datetime
import subprocess, json

from app.views.dashboard import dashboard
from app.models import Appointments, Transactions
from ...utils.report_revenue_datas import (
    get_report_data as get_revenue_data, 
    generate_insights as generate_revenue_insights
)
from ...utils.report_patients_datas import (
    get_report_data as get_patients_data,
    generate_patient_insights as generate_patient_insights
)

from ...utils.report_marketing_data import (
    get_report_data as get_marketing_data,
    generate_marketing_insights as generate_marketing_insights
)
from ...utils.report_inventory_data import (
    get_inventory_report_data as get_inventory_data,
)

@dashboard.route('/reports')    
def reports():
    today = datetime.now()
    selected_year = request.args.get('selected_year', type=int) or today.year
    selected_branch = request.args.get('branch', 'all')
    revenue_data = get_revenue_data(selected_year, selected_branch)
    revenue_insights = generate_revenue_insights(revenue_data)

    return render_template('/dashboard/reports.html',
                           labels=revenue_data['months'],
                           today_revenue=revenue_data['today_revenue'],
                           values=revenue_data['monthly_revenue'],
                           total_revenue=sum(revenue_data['monthly_revenue']),
                           forecast_values=revenue_data['forecast_values'],
                           current_month_revenue=revenue_data['current_month_revenue'],
                           selected_year=selected_year,
                           selected_branch=selected_branch,
                           current_year=today.year,
                           stacked_datasets=revenue_data['stacked_datasets'],
                           insight_text=revenue_insights)

@dashboard.route('/report_patients') 
def report_patients():
    today = datetime.now()
    current_month = today.month
    selected_year = request.args.get('selected_year', type=int) or today.year
    selected_branch = request.args.get('branch', 'all')
    patients_data = get_patients_data(selected_year, selected_branch)
    
    return render_template('/dashboard/report_patient.html',
                           months_labels=patients_data['months'],
                           service_labels=patients_data['services'],
                           values=patients_data['monthly_appointments'],
                           new_returning_stacked_datasets=patients_data['new_returning_datasets'],
                           forecast_values=patients_data['forecast_values'],
                           new_vs_returning_by_age=patients_data['new_vs_returning_by_age'],  
                           forecast_chart_data=patients_data['forecast_chart_data'],  
                           current_year=today.year,
                           selected_year=selected_year,
                           selected_branch=selected_branch,
                           current_month_new_patient=patients_data['monthly_new_patients'][current_month - 1],
                           current_month_returning_patient=patients_data['monthly_returning_patients'][current_month - 1],
                           current_month_appointment=patients_data['monthly_appointments'][current_month - 1],                        
                           insight_text=generate_patient_insights(patients_data))
       
@dashboard.route('/report_marketing')
def report_marketing():
    today = datetime.now()
    selected_year = request.args.get('selected_year', type=int) or today.year
    selected_branch = request.args.get('branch', 'all')
    current_month = datetime.today().month
    report_data = get_marketing_data(selected_year, selected_branch)

    return render_template(
        '/dashboard/report_marketing.html',
        current_year=today.year,  # <-- pass real current year
        selected_year=selected_year,
        popular_service_by_age=report_data['popular_services_by_age_bracket'],
        popular_service_by_gender=report_data['popular_services_by_gender'],
        insight_text=generate_marketing_insights(report_data, current_month)
    )

@dashboard.route('/report_inventory') 
def report_inventory():
    today = datetime.now()
    selected_year = request.args.get('selected_year', type=int) or today.year
    selected_branch = request.args.get('selected_branch', 'all')
    data = get_inventory_data(selected_branch)
    return render_template(
        'dashboard/report_inventory.html',
        low_stock=data['low_stock'],
        out_of_stock=data['out_of_stock'],
        expired=data['expired'],
        inventory_report_data=data,
        current_year=today.year, 
        selected_year=selected_year,
    )

@dashboard.route('/service_trend_forecast')
def service_trend_forecast():
    # 1. Get query params from frontend
    selected_branch = request.args.get("branch", type=str)

    # 2. Build query with filters
    query = Appointments.query.with_entities(
        Appointments.appointment_date,
        Appointments.appointment_category
    )

    if selected_branch:
        query = query.filter(Appointments.branch == selected_branch)

    appointments = query.all()

    # 3. Convert to list of dicts
    data = [
        {"appointment_date": str(a.appointment_date), "appointment_category": a.appointment_category}
        for a in appointments
    ]

    # 4. Convert Python list → JSON string
    json_input = json.dumps(data)

    # 5. Call R script
    result = subprocess.run(
        ["Rscript", "app/scripts/forecast_marketing.R"],
        input=json_input,
        text=True,
        capture_output=True
    )

    # 6. Handle errors
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    # 7. Parse R output JSON
    forecast_results = json.loads(result.stdout)

    return jsonify(forecast_results)

@dashboard.route('/revenue_forecast')
def revenue_forecast():
    # 1. Get query params from frontend
    selected_branch = request.args.get("branch", type=str)

    # 2. Build query with filters
    query = Transactions.query.with_entities(
        Transactions.transaction_datetime,
        Transactions.total_amount_paid
    )

    if selected_branch:
        query = query.filter(Transactions.branch == selected_branch)

    transactions = query.all()

    # 3. Convert to list of dicts
    # 3. Convert to list of dicts (cast Decimal to float)
    data = [
        {
            "transaction_datetime": str(t.transaction_datetime),
            "total_amount_paid": float(t.total_amount_paid) if t.total_amount_paid is not None else 0.0
        }
        for t in transactions
    ]

    # 4. Convert Python list → JSON string
    json_input = json.dumps(data)

    # 5. Call R script
    result = subprocess.run(
        ["Rscript", "app/scripts/forecast_revenue.R"],
        input=json_input,
        text=True,
        capture_output=True
    )

    # 6. Handle errors
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    # 7. Parse R output JSON
    forecast_results = json.loads(result.stdout)

    return jsonify(forecast_results)  
               
@dashboard.route('/patient_forecast')
def patient_forecast():
    # 1. Get query params from frontend
    selected_branch = request.args.get("branch", type=str)

    # 2. Build query with filters
    query = Appointments.query.with_entities(
        Appointments.appointment_date,
        Appointments.appointment_id
    )

    if selected_branch:
        query = query.filter(Appointments.branch == selected_branch)

    appointments = query.all()

    # 3. Convert to list of dicts
    # 3. Convert to list of dicts (cast Decimal to float)
    data = [
        {
            "appointment_date": str(a.appointment_date),
            "appointment_id": float(a.appointment_id) 
        }
        for a in appointments
    ]

    # 4. Convert Python list → JSON string
    json_input = json.dumps(data)

    # 5. Call R script
    result = subprocess.run(
        ["Rscript", "app/scripts/forecast_patient.R"],
        input=json_input,
        text=True,
        capture_output=True
    )

    # 6. Handle errors
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    # 7. Parse R output JSON
    forecast_results = json.loads(result.stdout)

    return jsonify(forecast_results)  