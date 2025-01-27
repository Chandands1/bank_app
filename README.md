# Bank Management Application

This is a simple Flask-based web application for managing bank and contact information. It allows you to add, edit, and view bank and contact details, with automatic tracking of modifications via timestamps.

## Features

- Add Bank Master details (Bank Name, Short Name, Location)
- Add Bank Contact details (Contact Name, Designation, Email, Location, Jurisdiction)
- Edit existing Bank and Contact details
- View all Banks and Contacts in the system
- Timestamps for creation and modification

## Technologies Used

- **Flask**: Web framework for building the application.
- **SQLAlchemy**: ORM for interacting with the SQLite database.
- **SQLite**: A lightweight database to store bank and contact details.
- **HTML/CSS**: For creating the user interface.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- Pip (Python package installer)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/bank-management-app.git
   cd bank-management-app
