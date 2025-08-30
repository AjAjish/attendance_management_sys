from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User

def base(request):
    return render(request, 'base/base.html')

def home(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'home.html', {'id': id})
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debugging line
        try:
            # To check existing user
            user = User.objects.get(username=username)
            if user.password == password:  
                id = str(user.id)
                # Make it userid on session for after login
                request.session['id'] = id
                messages.success(request, 'Login successful!')
                return redirect('dashboard_with_id', id=id)
            # Check if user is admin
            elif user.role == "admin" and user.password == password:
                id = str(user.id)
                request.session['id'] = id
                messages.success(request, 'Login successful!')
                return redirect('dashboard_with_id', id=id)
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

def dashboard(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'dashboard.html', {'id': id})
    return render(request, 'dashboard.html')

def student(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'student.html', {'id': id})
    return render(request, 'student.html')

def manage(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'manage.html', {'id': id})
    return render(request, 'manage.html')

def logout(request):
    # Clear the session data
    request.session.flush()
    messages.success(request, 'Logout successful!')
    return redirect('home')