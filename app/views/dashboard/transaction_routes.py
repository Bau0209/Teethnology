from flask import render_template, request, g

from app.views.dashboard import dashboard
from app.models import Procedures, Transactions, Appointments
from app import db

@dashboard.route('/transactions')
def transactions():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    # Start query and join relationships so we can filter by branch
    query = (
        db.session.query(Transactions)
        .join(Transactions.procedure)          # Transactions → Procedures
        .join(Procedures.appointment)          # Procedures → Appointments
    )

    if selected_branch != 'all':
        query = query.filter(Appointments.branch_id == selected_branch)

    # Paginate the query
    items = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        '/dashboard/transactions.html',
        transactions=items.items,
        pagination=items
    )


from sqlalchemy import func

from sqlalchemy import func

@dashboard.route('/balance_record')
def balance_record():
    selected_branch = g.get('selected_branch', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Subquery: total payments per procedure
    subquery = (
        db.session.query(
            Transactions.procedure_id,
            func.coalesce(func.sum(Transactions.total_amount_paid), 0).label("paid")
        )
        .group_by(Transactions.procedure_id)
        .subquery()
    )

    # Base query: procedures + payments
    query = (
        db.session.query(Procedures, subquery.c.paid)
        .outerjoin(subquery, Procedures.procedure_id == subquery.c.procedure_id)
        .join(Procedures.appointment)  # join to appointment so we can filter by branch
    )

    # Apply branch filter if not 'all'
    if selected_branch != 'all':
        query = query.filter(Appointments.branch_id == selected_branch)

    # Only show balances where remaining > 0
    query = query.filter(Procedures.fee > subquery.c.paid)

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Build balance data
    balance_data = []
    for proc, paid in pagination.items:
        remaining = float(proc.fee) - float(paid or 0)
        balance_data.append({
            "patient": proc.patient,
            "last_visit": proc.procedure_date,
            "total_fee": proc.fee,
            "amount_paid": float(paid or 0),
            "remaining": remaining,
        })

    return render_template(
        "/dashboard/balance_records.html",
        balance_data=balance_data,
        pagination=pagination
    )


@dashboard.route('/patient/<int:patient_id>/payment-history')
def payment_history(patient_id):
    balance_data = Procedures.query.filter_by(patient_id=patient_id).all()
    return render_template("your_template.html", balance_data=balance_data)