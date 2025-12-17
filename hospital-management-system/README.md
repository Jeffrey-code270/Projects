# Hospital Management System (HMS)

Mini hospital management web app with doctor availability, patient booking, and serverless email notifications.

## Features
- Role-based authentication (Doctor/Patient)
- Doctor availability management
- Patient appointment booking with race condition prevention
- Email notifications (welcome, booking, cancellation)
- Google Calendar integration
- Responsive Bootstrap UI

## Tech Stack
- **Backend**: Django 4.2.7
- **Database**: SQLite (demo) / PostgreSQL (production)
- **Email**: Serverless AWS Lambda function
- **Frontend**: Bootstrap 5 + JavaScript

## Quick Start

```bash
python3 setup.py          # Install & setup
python3 start_hms.py       # Start both services
```

**Demo Accounts:**
- Doctor: `dr_smith` / `demo123`
- Patient: `patient_doe` / `demo123`

**URLs:**
- App: http://localhost:8000
- Email service: http://localhost:3000

## Usage

**Doctors:** Sign up → Create availability slots → Manage bookings

**Patients:** Sign up → Browse doctors → Book appointments

## Project Structure
```
hms/
├── accounts/          # Authentication
├── appointments/      # Booking system
├── email_service/     # Serverless emails
├── templates/         # HTML templates
└── manage.py         # Django management
```

## License
MIT License