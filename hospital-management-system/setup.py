#!/usr/bin/env python3
"""
Setup script for Hospital Management System
"""
import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("Setting up Hospital Management System...")
    
    # Install Python dependencies
    print("\n1. Installing Python dependencies...")
    if not run_command("python3 -m pip install -r requirements.txt"):
        print("Failed to install Python dependencies")
        return False
    
    # Run Django migrations
    print("\n2. Running Django migrations...")
    if not run_command("python3 manage.py makemigrations"):
        print("Failed to create migrations")
        return False
    
    if not run_command("python3 manage.py migrate"):
        print("Failed to run migrations")
        return False
    
    # Create superuser (optional)
    print("\n3. Creating superuser (optional)...")
    print("You can create a superuser account for admin access:")
    print("Run: python3 manage.py createsuperuser")
    
    # Setup email service
    print("\n4. Setting up email service...")
    email_service_dir = "email_service"
    
    # Install Node.js dependencies for serverless
    if os.path.exists(email_service_dir):
        print("Installing serverless dependencies...")
        if not run_command("npm install", cwd=email_service_dir):
            print("Failed to install serverless dependencies")
            print("Make sure Node.js and npm are installed")
    
    print("\n✅ Setup completed!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Start the Django server: python3 manage.py runserver")
    print("3. Start the email service: cd email_service && npm start")
    print("4. Visit http://localhost:8000 to access the application")

if __name__ == "__main__":
    main()