#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("Setting up Hospital Management System...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        subprocess.run([sys.executable, "demo.py"], check=True)
        
        print("\n✅ Setup completed!")
        print("Start: python3 manage.py runserver")
        print("Email service: python3 mock_email_service.py")
        print("Visit: http://localhost:8000")
        
    except subprocess.CalledProcessError as e:
        print(f"Setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()