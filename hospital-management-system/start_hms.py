#!/usr/bin/env python3
"""
Startup script for Hospital Management System
Starts both Django server and mock email service
"""
import subprocess
import sys
import time
import threading
import os

def start_django_server():
    """Start Django development server"""
    print("🚀 Starting Django server...")
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n👋 Django server stopped")

def start_email_service():
    """Start mock email service"""
    print("📧 Starting email service...")
    time.sleep(2)  # Wait a bit for Django to start
    try:
        subprocess.run([sys.executable, 'mock_email_service.py'])
    except KeyboardInterrupt:
        print("\n👋 Email service stopped")

def main():
    print("🏥 Hospital Management System Startup")
    print("=====================================")
    
    # Check if demo data exists
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
        django.setup()
        
        from accounts.models import User
        if not User.objects.filter(username='dr_smith').exists():
            print("📊 Creating demo data...")
            subprocess.run([sys.executable, 'demo.py'])
    except:
        pass
    
    print("\n🎯 Starting services...")
    print("- Django server will run on: http://localhost:8000")
    print("- Email service will run on: http://localhost:3000")
    print("\n📋 Demo Accounts:")
    print("- Doctor: dr_smith / demo123")
    print("- Patient: patient_doe / demo123")
    print("\nPress Ctrl+C to stop all services\n")
    
    # Start email service in background thread
    email_thread = threading.Thread(target=start_email_service, daemon=True)
    email_thread.start()
    
    # Start Django server in main thread
    try:
        start_django_server()
    except KeyboardInterrupt:
        print("\n👋 Shutting down HMS...")

if __name__ == "__main__":
    main()