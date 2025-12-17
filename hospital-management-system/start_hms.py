#!/usr/bin/env python3
import subprocess
import sys
import threading
import time

def start_email_service():
    time.sleep(2)
    subprocess.run([sys.executable, 'mock_email_service.py'])

def main():
    print("🏥 Starting HMS...")
    print("Django: http://localhost:8000")
    print("Email: http://localhost:3000")
    print("Login: dr_smith/demo123 or patient_doe/demo123\n")
    
    threading.Thread(target=start_email_service, daemon=True).start()
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n👋 HMS stopped")

if __name__ == "__main__":
    main()