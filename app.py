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
        
        new_bank = BankMaster(
            bank_name=bank_name, 
            bank_short_name=bank_short_name, 
            location=location
        )
        db.session.add(new_bank)
        db.session.commit()
        return redirect(url_for('view_data'))
    
    return render_template('bank_master.html')

@app.route('/add-bank-contact', methods=['GET', 'POST'])
def add_bank_contact():
    banks = BankMaster.query.all()  # Fetch all banks for dropdown
    if request.method == 'POST':
        locations = request.form.getlist('location[]')
        contact_names = request.form.getlist('contact_name[]')
        contact_phs = request.form.getlist('contact_ph[]')
        contact_emails = request.form.getlist('contact_email[]')
        email_thresholds = request.form.getlist('email_threshold[]')
        jurisdictions = request.form.getlist('jurisdiction[]')
        bank_ids = request.form.getlist('bank_id[]')

        for i in range(len(locations)):
            new_contact = BankContactDetails(
                location=locations[i],
                contact_name=contact_names[i],
                contact_designation="N/A",  # Adjust if needed
                contact_email=contact_emails[i],
                email_size_threshold=int(email_thresholds[i]) if email_thresholds[i] else 0,
                contact_jurisdiction=jurisdictions[i],
                contact_bank_slno=int(bank_ids[i]) if bank_ids[i] else None
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
        # Check for missing bank_id and handle accordingly
        bank_id = request.form.get('bank_id')  # Use .get to avoid KeyError

        # If bank_id is not present in the form, handle accordingly
        if bank_id:
            contact.contact_bank_slno = int(bank_id)
        else:
            contact.contact_bank_slno = None  # Or handle as needed

        contact.location = request.form['location']
        contact.contact_name = request.form['contact_name']
        contact.contact_designation = request.form['contact_designation']
        contact.contact_email = request.form['contact_email']
        contact.email_size_threshold = int(request.form['email_threshold']) if request.form['email_threshold'] else 0
        contact.contact_jurisdiction = request.form['jurisdiction']
        contact.modified_on = datetime.utcnow()

        db.session.commit()
        return redirect(url_for('view_data'))

    return render_template('edit_contact.html', contact=contact, banks=banks)

if __name__ == '__main__':
    app.run(debug=True)
