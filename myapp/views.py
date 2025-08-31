from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User,Student
import json
from datetime import datetime

def base(request):
    return render(request, 'base/base.html')

def home(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'home.html', {'user': user})
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
                messages.error(request, 'Invalid username or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

def dashboard(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'dashboard.html', {'user': user})
    return render(request, 'dashboard.html')

def student(request, id=None):
    years = [2, 3, 4]
    students = Student.objects.all() 

    if request.method == 'POST':
        year = request.POST.get('year')
        section = request.POST.get('section')

        if year and section: 
            students = Student.objects.filter(year=year, class_section=section)

        user_id = request.session.get('id')
        user = User.objects.get(id=user_id) if user_id else None

        return render(request, 'student.html', {
            'user': user,
            'students': students,
            'years': years
        })

    # GET Request – just load the page with years and user
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id) if user_id else None

    return render(request, 'student.html', {
        'user': user,
        'students': students, 
        'years': years
    })

def manage(request, id=None):
    years = [2, 3, 4]
    students = None

    if request.method == 'POST':
        # Extract year, section, and attendance JSON payload
        year = request.POST.get('year')
        section = request.POST.get('section')
        attendance_json = request.POST.get('attendance_payload')  # Hidden field with JSON

        if attendance_json:
            try:
                attendance_data = json.loads(attendance_json)

                date = attendance_data.get("date")
                year = attendance_data.get("year")
                section = attendance_data.get("section")
                items = attendance_data.get("items", [])

                for item in items:
                    roll = item.get("roll")
                    status = item.get("status")

                    try:
                        student = Student.objects.get(roll_number=roll, year=year, class_section=section)
                        # Get or initialize the attendance_record
                        record = student.attendance_record or {}

                        # Ensure date key exists
                        if date not in record:
                            record[date] = {}

                        # Update attendance for that roll
                        record[date][roll] = status

                        student.attendance_record = record
                        student.attendance = status  # Update current attendance status
                        student.save()

                    except Student.DoesNotExist:
                        continue  # Skip missing students gracefully

            except json.JSONDecodeError:
                pass  # Handle invalid JSON silently or log error

        # After marking attendance, fetch students again for UI refresh
        if year and section:
            students = Student.objects.filter(year=year, class_section=section)

        user_id = request.session.get('id')
        user = User.objects.get(id=user_id) if user_id else None

        return render(request, 'manage.html', {
            'user': user,
            'students': students,
            'years': years
        })

    # GET Request – just load the page
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id) if user_id else None

    return render(request, 'manage.html', {
        'user': user,
        'students': students,
        'years': years
    })

def logout(request):
    # Clear the session data
    request.session.flush()
    messages.success(request, 'Logout successful!')
    return redirect('home')