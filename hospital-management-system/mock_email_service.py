#!/usr/bin/env python3
"""
Mock email service for testing HMS without serverless setup
Runs a simple HTTP server that mimics the serverless email function
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class EmailServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/dev/send-email':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'Email service running', 'endpoints': ['/dev/send-email']}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/dev/send-email':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                action = data.get('action')
                to_email = data.get('to_email')
                
                print(f"\n📧 Email Service Called:")
                print(f"Action: {action}")
                print(f"To: {to_email}")
                
                if action == 'SIGNUP_WELCOME':
                    print(f"Welcome email for {data.get('user_name')} ({data.get('user_type')})")
                elif action == 'BOOKING_CONFIRMATION':
                    print(f"Booking confirmation for {data.get('patient_name')}")
                    print(f"Doctor: Dr. {data.get('doctor_name')}")
                    print(f"Date: {data.get('date')} at {data.get('time')}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {'message': 'Email sent successfully (mock)'}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_mock_email_service():
    server_address = ('localhost', 3000)
    httpd = HTTPServer(server_address, EmailServiceHandler)
    print("🚀 Mock Email Service running on http://localhost:3000")
    print("📧 Email notifications will be logged here")
    print("Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Mock Email Service stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_mock_email_service()