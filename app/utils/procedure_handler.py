from app.models import Procedures, Transactions
from datetime import datetime, date
from app import db

def create_procedure(appointment_id, treatment_procedure, tooth_area, provider, treatment_plan, fee, appointment_date):
    procedure = Procedures(
        appointment_id=appointment_id,
        procedure_date=appointment_date,
        treatment_procedure=treatment_procedure,
        tooth_area=tooth_area,
        provider=provider,
        treatment_plan=treatment_plan,
        fee=fee,
        procedure_status='completed',
        notes='Recorded via modal'
    )
    db.session.add(procedure)
    db.session.flush()  # Keep procedure.procedure_id available before commit
    return procedure

def create_transaction(procedure_id, treatment_procedure, provider, payment_method, total_paid, receipt_path=None):
    transaction = Transactions(
        procedure_id=procedure_id,
        receipt_number=f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        payment_method=payment_method,
        transaction_datetime=datetime.now(),
        dentist_name=provider,
        service_detail=treatment_procedure,
        total_amount_paid=total_paid,
        transaction_image_link=receipt_path
    )
    db.session.add(transaction)
    return transaction
