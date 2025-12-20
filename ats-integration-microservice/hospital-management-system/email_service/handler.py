import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        action = body.get('action')
        to_email = body.get('to_email')
        
        if not action or not to_email:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required fields'})
            }
        
        # Prepare email content based on action
        if action == 'SIGNUP_WELCOME':
            subject = 'Welcome to Hospital Management System'
            html_content = f"""
            <h2>Welcome to HMS!</h2>
            <p>Hello {body.get('user_name', 'User')},</p>
            <p>Your account has been successfully created as a <strong>{body.get('user_type', 'user')}</strong>.</p>
            <p>You can now log in and start using the Hospital Management System.</p>
            <p>Best regards,<br>HMS Team</p>
            """
        
        elif action == 'BOOKING_CONFIRMATION':
            subject = 'Appointment Confirmation'
            html_content = f"""
            <h2>Appointment Confirmed!</h2>
            <p>Hello {body.get('patient_name', 'Patient')},</p>
            <p>Your appointment has been successfully booked:</p>
            <ul>
                <li><strong>Doctor:</strong> Dr. {body.get('doctor_name', 'N/A')}</li>
                <li><strong>Date:</strong> {body.get('date', 'N/A')}</li>
                <li><strong>Time:</strong> {body.get('time', 'N/A')}</li>
            </ul>
            <p>Please arrive 10 minutes before your scheduled time.</p>
            <p>Best regards,<br>HMS Team</p>
            """
        
        elif action == 'BOOKING_CANCELLATION':
            subject = 'Appointment Cancelled'
            html_content = f"""
            <h2>Appointment Cancelled</h2>
            <p>Hello {body.get('patient_name', 'Patient')},</p>
            <p>We regret to inform you that your appointment has been cancelled:</p>
            <ul>
                <li><strong>Doctor:</strong> Dr. {body.get('doctor_name', 'N/A')}</li>
                <li><strong>Date:</strong> {body.get('date', 'N/A')}</li>
                <li><strong>Time:</strong> {body.get('time', 'N/A')}</li>
            </ul>
            <p>Please book a new appointment at your convenience.</p>
            <p>We apologize for any inconvenience caused.</p>
            <p>Best regards,<br>HMS Team</p>
            """
        
        else:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Invalid action'})
            }
        
        # Send email
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        
        if not smtp_user or not smtp_password:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'SMTP credentials not configured'})
            }
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Email sent successfully'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }