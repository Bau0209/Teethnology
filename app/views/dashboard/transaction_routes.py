from flask import render_template

from app.views.dashboard import dashboard
from app.models import Procedures, Transactions

@dashboard.route('/transactions')
def transactions():
    transactions = Transactions.query.all()
    return render_template('/dashboard/transactions.html', transactions=transactions)

@dashboard.route('/balance_record')
def balance_record():
    # Get all procedures
    procedures = Procedures.query.all()
    balance_data = []

    for proc in procedures:
        total_fee = proc.fee
        payments = sum(t.total_amount_paid for t in proc.transactions)
        remaining = float(total_fee) - float(payments)

        if remaining > 0:  # Show only patients with balance
            balance_data.append({
                'patient': proc.patient,
                'last_visit': proc.procedure_date,
                'total_fee': total_fee,
                'amount_paid': payments,
                'remaining': remaining
            })

    return render_template('/dashboard/balance_records.html', balance_data=balance_data)
