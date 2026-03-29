from django.shortcuts import render

def landing(request):
    return render(request, 'login.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def log_mood_view(request):
    return render(request, 'log_mood.html')

def analytics_view(request):
    return render(request, 'analytics.html')