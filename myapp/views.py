from django.shortcuts import render

def home(request):
    return render(request, 'base/base.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def student(request):
    return render(request, 'student.html')

def manage(request):
    return render(request, 'manage.html')