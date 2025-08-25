from app import db

class Procedures(db.Model):
    __tablename__ = 'procedure_history'

    procedure_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey('appointments.appointment_id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=True
    )

    procedure_date = db.Column(db.Date, nullable=False)
    tooth_area = db.Column(db.String(10), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    procedure_status = db.Column(db.String(255))
    notes = db.Column(db.Text)

    # Relationship to Appointments (no backref to avoid name conflict)
    appointment = db.relationship('Appointments', lazy=True)

    @property
    def patient(self):
        """Access patient through the linked appointment."""
        return self.appointment.patient if self.appointment else None
