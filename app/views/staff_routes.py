from flask import Blueprint, render_template

staff = Blueprint('staff', __name__)

@staff.route('/staff_home')
def staff_home():
    return render_template('/staff/s_Home.html')

@staff.route('/appointment')
def appointment():
   return render_template('/staff/s_appointment.html')

@staff.route('/appointment_request')
def appointment_request():
   return render_template('/staff/s_appointment_req.html')

@staff.route('/patients')
def patients():
   return render_template('/staff/s_patient.html')

@staff.route('/patient_info')
def patient_info():
   return render_template('/staff/s_patient_info.html')

@staff.route('/patient_procedure')
def patient_procedure():
   return render_template('/staff/s_procedure.html')

@staff.route('/patient_dental_rec')
def patient_dental_rec():
   return render_template('/staff/s_dental_rec.html')

@staff.route('/transaction')
def transaction():
   return render_template('/staff/s_transaction.html')

@staff.route('/balance_record')
def balance_record():
   return render_template('/staff/s_balance_rec.html')