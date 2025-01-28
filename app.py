from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, BankMaster, BankContactDetails

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables before handling requests
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/add-bank-master', methods=['GET', 'POST'])
def add_bank_master():
    if request.method == 'POST':
        bank_name = request.form['bank_name']
        bank_short_name = request.form['bank_short_name']
        location = request.form['location']
        new_bank = BankMaster(bank_name=bank_name, bank_short_name=bank_short_name, location=location)
        db.session.add(new_bank)
        db.session.commit()
        return redirect(url_for('view_data'))
    return render_template('bank_master.html')

@app.route('/add-bank-contact', methods=['GET', 'POST'])
def add_bank_contact():
    banks = BankMaster.query.all()  # Fetch all banks for dropdown
    if request.method == 'POST':
        location = request.form['location']
        contact_name = request.form['contact_name']
        contact_designation = request.form['contact_designation']
        contact_email = request.form['contact_email']
        email_threshold = request.form['email_threshold']
        jurisdiction = request.form['jurisdiction']
        bank_id = request.form['bank_id']
        new_contact = BankContactDetails(
            location=location,
            contact_name=contact_name,
            contact_designation=contact_designation,
            contact_email=contact_email,
            email_size_threshold=email_threshold,
            contact_jurisdiction=jurisdiction,
            contact_bank_slno=bank_id
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('view_data'))
    return render_template('bank_contact.html', banks=banks)

@app.route('/view-data')
def view_data():
    banks = BankMaster.query.all()
    contacts = BankContactDetails.query.all()
    return render_template('view_data.html', banks=banks, contacts=contacts)

@app.route('/edit-bank-master/<int:bank_id>', methods=['GET', 'POST'])
def edit_bank_master(bank_id):
    bank = BankMaster.query.get(bank_id)

    if request.method == 'POST':
        bank.bank_name = request.form['bank_name']
        bank.bank_short_name = request.form['bank_short_name']
        bank.location = request.form['location']
        bank.modified_on = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('view_data'))

    return render_template('edit_bank.html', bank=bank)

@app.route('/edit-bank-contact/<int:contact_id>', methods=['GET', 'POST'])
def edit_bank_contact(contact_id):
    contact = BankContactDetails.query.get(contact_id)
    banks = BankMaster.query.all()  # Fetch banks for dropdown

    if request.method == 'POST':
        contact.location = request.form['location']
        contact.contact_name = request.form['contact_name']
        contact.contact_designation = request.form['contact_designation']
        contact.contact_email = request.form['contact_email']
        contact.email_size_threshold = request.form['email_threshold']
        contact.contact_jurisdiction = request.form['jurisdiction']
        contact.contact_bank_slno = request.form['bank_id']
        contact.modified_on = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('view_data'))

    return render_template('edit_contact.html', contact=contact, banks=banks)

if __name__ == '__main__':
    app.run(debug=True)
