from collections import defaultdict
from datetime import date, datetime
from app import db
from sqlalchemy import func, extract

from app.models import Transactions, Appointments, Procedures

months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

def get_today_revenue():
    today = date.today()
    return db.session.query(func.sum(Transactions.total_amount_paid))\
        .filter(func.date(Transactions.transaction_datetime) == today)\
        .scalar() or 0
    
def get_monthly_revenue(year):
    data = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        func.sum(Transactions.total_amount_paid).label('total')
    ).filter(
        extract('year', Transactions.transaction_datetime) == year
    ).group_by('month').order_by('month').all()
    
    values = [0] * 12
    for month, total in data:
        values[int(month) - 1] = float(total)
    
    return values

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

def get_service_month_data(year):
    return db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        Appointments.appointment_category,
        func.sum(Transactions.total_amount_paid).label('total')
    ).join(
        Procedures, Procedures.procedure_id == Transactions.procedure_id
    ).join(
        Appointments, Appointments.appointment_id == Procedures.appointment_id
    ).filter(
        extract('year', Transactions.transaction_datetime) == year
    ).group_by(
        'month', Appointments.appointment_category
    ).order_by(
        'month'
    ).all()
    
def prepare_chart_datasets(service_month_data):
    service_monthly_totals = defaultdict(lambda: [0]*12)
    for month, service, total in service_month_data:
        service_monthly_totals[service][int(month) - 1] = float(total)
    
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1',
              '#17a2b8', '#6610f2', '#fd7e14', '#20c997', '#6c757d']
    
    stacked_datasets = []
    for i, (service, totals) in enumerate(service_monthly_totals.items()):
        stacked_datasets.append({
            'label': service,
            'data': totals,
            'backgroundColor': colors[i % len(colors)]
        })
    return stacked_datasets

def get_report_data(selected_year, current_month):
    monthly_revenue = get_monthly_revenue(selected_year)
    today_revenue = get_today_revenue()
    service_month_data = get_service_month_data(selected_year)
    stacked_datasets = prepare_chart_datasets(service_month_data)

    return {
        'months': months,
        'monthly_revenue': monthly_revenue,
        'today_revenue': today_revenue,
        'current_month_revenue': get_monthly_revenue(date.today().year)[current_month - 1],
        'service_month_data': service_month_data,
        'stacked_datasets': stacked_datasets,
        'forecast_values': moving_average_forecast(monthly_revenue, window=5)
    }
    
def generate_insights(data):
    current_month = datetime.now().month
    insights = []

    # Insight 1: Revenue
    revenue = data['current_month_revenue']
    revenue_msg = ["<strong>Revenues:</strong>"]
    if revenue < 10000:
        revenue_msg.append("Revenue is below ₱10,000. Consider promoting top services.")
    elif revenue < 20000:
        revenue_msg.append("Fair revenue. Highlight best-sellers to boost earnings.")
    else:
        revenue_msg.append("Strong revenue this month! Keep it up.")
    insights.append("<br>".join(revenue_msg))

    # Insight 2: Top service
    service_msg = ["<strong>Services:</strong>"]
    current_services = [
        s for s in data['service_month_data'] if int(s.month) == current_month
    ]
    if current_services:
        top_service = max(current_services, key=lambda x: x.total)
        service_msg.append(f"Top earning service: {top_service.appointment_category}. Upsell related procedures.")
    else:
        service_msg.append("No services recorded this month.")
    insights.append("<br>".join(service_msg))

    return "<br><br>".join(insights)