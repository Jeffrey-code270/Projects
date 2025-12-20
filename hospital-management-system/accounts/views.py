from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm
import requests
from django.conf import settings

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('appointments:dashboard')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Send welcome email via serverless function
            try:
                email_data = {
                    'action': 'SIGNUP_WELCOME',
                    'to_email': user.email,
                    'user_name': user.username,
                    'user_type': user.user_type
                }
                requests.post(settings.EMAIL_SERVICE_URL, json=email_data, timeout=5)
            except:
                pass  # Email service failure shouldn't block signup
            
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('appointments:dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})