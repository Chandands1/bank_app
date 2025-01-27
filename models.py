from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BankMaster(db.Model):
    __tablename__ = 'bank_master'

    bank_slno = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100))
    bank_short_name = db.Column(db.String(10))
    location = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BankContactDetails(db.Model):
    __tablename__ = 'bank_contact_details'

    contact_slno = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    contact_name = db.Column(db.String(100))
    contact_designation = db.Column(db.String(30))
    contact_email = db.Column(db.String(100))
    email_size_threshold = db.Column(db.Integer)
    contact_jurisdiction = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contact_bank_slno = db.Column(db.Integer, db.ForeignKey('bank_master.bank_slno'))
