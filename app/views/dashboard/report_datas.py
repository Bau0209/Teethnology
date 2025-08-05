from collections import defaultdict
from datetime import date
from app import db
from sqlalchemy import func, extract

from app.models import Transactions, Appointments

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

def get_appointments_count(month):
    return db.session.query(func.count(Appointments.appointment_id))\
        .filter(extract('month', Appointments.appointment_date) == month)\
        .scalar()
        
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
