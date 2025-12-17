# Hospital Management System (HMS)

A mini hospital management web application focused on doctor availability and patient appointment booking, with serverless email notifications and Google Calendar integration.

## Features

### User Roles
- **Doctors**: Can sign up, set availability slots, and manage bookings
- **Patients**: Can sign up, view doctors, and book available appointments

### Core Functionality
- ✅ Role-based authentication (Doctor/Patient)
- ✅ Doctor availability management
- ✅ Patient appointment booking
- ✅ Race condition prevention for bookings
- ✅ Google Calendar integration
- ✅ Serverless email notifications
- ✅ Responsive web interface

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (for demo) / PostgreSQL (production)
- **Authentication**: Django built-in with custom User model
- **Email Service**: AWS Lambda with Serverless Framework
- **Calendar**: Google Calendar API
- **Frontend**: Bootstrap 5 + vanilla JavaScript

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for serverless email service)
- Git

### Installation

1. **Clone and setup the project:**
   ```bash
   cd "/Users/apple/IdeaProjects/beginning/python project"
   python3 setup.py
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start the Django server:**
   ```bash
   python3 manage.py runserver
   ```

4. **Start the email service (in another terminal):**
   ```bash
   cd email_service
   npm start
   ```

5. **Access the application:**
   - Main app: http://localhost:8000
   - Email service: http://localhost:3000

## Usage

### For Doctors
1. Sign up as a "Doctor"
2. Login to access doctor dashboard
3. Create availability slots with date and time
4. View your bookings and availability

### For Patients
1. Sign up as a "Patient"
2. Login to access patient dashboard
3. Select a doctor to view available slots
4. Book an appointment slot

### Email Notifications
- Welcome email on signup
- Confirmation email on booking
- Powered by serverless AWS Lambda function

### Google Calendar Integration
- Automatic calendar events for both doctor and patient
- OAuth2 authentication required
- Events include appointment details

## Project Structure

```
hms/
├── accounts/           # User authentication app
├── appointments/       # Booking and availability app
├── email_service/      # Serverless email function
├── templates/          # HTML templates
├── hms/               # Django project settings
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── setup.py          # Setup script
```

## API Endpoints

- `GET /accounts/login/` - Login page
- `GET /accounts/signup/` - Signup page
- `GET /dashboard/` - Role-based dashboard
- `POST /appointments/create-availability/` - Create availability (doctors)
- `POST /appointments/book/<id>/` - Book appointment (patients)
- `GET /appointments/api/doctor/<id>/slots/` - Get doctor's available slots

## Demo Video

Create a 10-minute screen recording showcasing:
1. User registration (doctor and patient)
2. Doctor creating availability slots
3. Patient booking appointments
4. Email notifications working
5. Calendar integration (if configured)
6. Code walkthrough

## Development Notes

- Uses SQLite for demo simplicity
- Email service runs on port 3000
- Django runs on port 8000
- Race conditions prevented with database locks
- Bootstrap for responsive UI
- Minimal code approach for core functionality

## Production Deployment

For production:
1. Switch to PostgreSQL database
2. Deploy email service to AWS Lambda
3. Configure proper Google OAuth2 credentials
4. Set up SMTP for email delivery
5. Use environment variables for all secrets

## License

MIT License - Feel free to use for educational purposes.