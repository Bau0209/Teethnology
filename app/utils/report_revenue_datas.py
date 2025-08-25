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

    # --- Insight 1: Current Revenue ---
    revenue = data['current_month_revenue']
    revenue_msg = ["<strong>Current Month Revenue:</strong>"]
    if revenue < 10000:
        revenue_msg.append(f"Revenue is low at ₱{revenue:,.2f}.")
    elif revenue < 20000:
        revenue_msg.append(f"Revenue is fair at ₱{revenue:,.2f}.")
    else:
        revenue_msg.append(f"Revenue is strong at ₱{revenue:,.2f}. Keep it up!")
    insights.append("<br>".join(revenue_msg))

    # --- Insight 2: Forecast Revenue (Next Month) ---
    forecast_values = data['forecast_values']
    if current_month < len(forecast_values):
        forecast_next = forecast_values[current_month]  # forecast for next month
    else:
        forecast_next = forecast_values[-1]  # fallback
    
    forecast_msg = ["<strong>Forecast (Next Month):</strong>"]
    if forecast_next < 10000:
        forecast_msg.append(f"Projected revenue may drop to ₱{forecast_next:,.2f}.")
    elif forecast_next < 20000:
        forecast_msg.append(f"Projected revenue is expected to be around ₱{forecast_next:,.2f}.")
    else:
        forecast_msg.append(f"Projected revenue may remain strong at ₱{forecast_next:,.2f}.")
    insights.append("<br>".join(forecast_msg))

    # --- Insight 3: Recommendations ---
    reco_msg = ["<strong>Recommendation:</strong>"]
    if revenue < 10000 and forecast_next < 10000:
        reco_msg.append("Double down on promotions and discounts to boost sales.")
    elif revenue < 20000 and forecast_next < 20000:
        reco_msg.append("Sustain efforts on best-selling services and explore new offers.")
    else:
        reco_msg.append("Maintain current strategies, but watch for seasonal demand shifts.")
    insights.append("<br>".join(reco_msg))

    return "<br><br>".join(insights)
