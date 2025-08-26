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
    
def get_monthly_revenue(year, branch):
    # Start query with joins
    query = db.session.query(
        extract('month', Transactions.transaction_datetime).label('month'),
        func.sum(Transactions.total_amount_paid).label('total')
    ).join(
        Procedures, Transactions.procedure_id == Procedures.procedure_id
    ).join(
        Appointments, Procedures.appointment_id == Appointments.appointment_id
    ).filter(
        extract('year', Transactions.transaction_datetime) == year
    )

    # Filter by branch_id if not "all"
    if branch and branch.isdigit():
        query = query.filter(Appointments.branch_id == int(branch))
    else:
        # Either skip filtering or handle default
        # e.g., show all branches if none selected
        pass

    # Group and order
    data = query.group_by('month').order_by('month').all()

    # Prepare 12-month values
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

def get_service_month_data(year, branch):
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

def get_report_data(selected_year, selected_branch):    
    current_month = datetime.now().month
    monthly_revenue = get_monthly_revenue(selected_year, selected_branch)
    today_revenue = get_today_revenue()
    service_month_data = get_service_month_data(selected_year, selected_branch)
    stacked_datasets = prepare_chart_datasets(service_month_data)

    return {
        'months': months,
        'monthly_revenue': monthly_revenue,
        'today_revenue': today_revenue,
        'current_month_revenue': get_monthly_revenue(date.today().year, selected_branch)[current_month - 1],
        'service_month_data': service_month_data,
        'stacked_datasets': stacked_datasets,
        'forecast_values': moving_average_forecast(monthly_revenue, window=5)
    }
    
def generate_insights(data):
    current_month = datetime.now().month
    insights = []

    # Calculate averages
    avg_revenue = sum(data['monthly_revenue']) / max(1, len([v for v in data['monthly_revenue'] if v > 0]))
    avg_forecast = sum(data['forecast_values']) / max(1, len([v for v in data['forecast_values'] if v > 0]))

    # Current Revenue
    revenue = data['current_month_revenue']
    if revenue < avg_revenue * 0.9:
        revenue_msg = f"Current revenue ₱{revenue:,.2f} is below the average ₱{avg_revenue:,.2f}."
    elif revenue > avg_revenue * 1.1:
        revenue_msg = f"Current revenue ₱{revenue:,.2f} is above the average ₱{avg_revenue:,.2f}."
    else:
        revenue_msg = f"Current revenue ₱{revenue:,.2f} is around the average ₱{avg_revenue:,.2f}."
    insights.append(f"<strong>Current Month Revenue:</strong><br>{revenue_msg}")

    # Forecast (Next Month)
    if current_month < len(data['forecast_values']):
        forecast_next = data['forecast_values'][current_month]
    else:
        forecast_next = data['forecast_values'][-1]

    if forecast_next < avg_forecast * 0.9:
        forecast_msg = f"Next month forecast ₱{forecast_next:,.2f} is below the average ₱{avg_forecast:,.2f}."
    elif forecast_next > avg_forecast * 1.1:
        forecast_msg = f"Next month forecast ₱{forecast_next:,.2f} is above the average ₱{avg_forecast:,.2f}."
    else:
        forecast_msg = f"Next month forecast ₱{forecast_next:,.2f} is around the average ₱{avg_forecast:,.2f}."
    insights.append(f"<strong>Forecast (Next Month):</strong><br>{forecast_msg}")

    # Recommendation with credible feedback
    reco_msg = ["<strong>Recommendation:</strong>"]
    if revenue < avg_revenue and forecast_next < avg_forecast:
        reco_msg.append(
            "Increase visibility through targeted promotions and seasonal offers.<br>"
            "Both current and forecasted revenues are trailing historical averages. "
            "This signals a consistent demand slowdown. Proactive action is needed to prevent revenue gaps."
        )
    elif revenue < avg_revenue and forecast_next >= avg_forecast:
        reco_msg.append(
            "Strengthen campaigns to capture the expected upswing next month.<br>"
            "Despite underperformance this month, forecasts suggest demand recovery. "
            "This indicates short-term weakness but improving momentum — preparation now ensures you capitalize on it."
        )
    elif revenue >= avg_revenue and forecast_next < avg_forecast:
        reco_msg.append(
            "Secure repeat business and protect against a potential dip.<br>"
            "Current revenue is strong but the forecast signals declining momentum. "
            "Retention strategies (loyalty programs, personalized offers) will help sustain stability."
        )
    else:
        reco_msg.append(
            "Maintain current strategy while optimizing operations for efficiency.<br>"
            "Both current and forecasted revenues are solid, showing steady growth. "
            "This is an ideal time to reinvest in high-performing services and scale what works."
        )
    insights.append("<br>".join(reco_msg))

    return "<br><br>".join(insights)


