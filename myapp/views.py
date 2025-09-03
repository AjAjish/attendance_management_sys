from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User,Student, AttendanceRecord
import json
from datetime import datetime
from django.http import JsonResponse


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
        # Extract year and section for filtering
        year = request.POST.get('year')
        section = request.POST.get('section')
        print(f"Filtering students for Year: {year}, Section: {section}")

        # After filtering, fetch students for UI display
        if year and section:
            students = Student.objects.filter(year=year, class_section=section)

    # Get user from session for rendering
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


def submit_attendance(request,id=None):
    if request.method == "POST":
        try:
            user = User.objects.get(id=id)
            attendance_data = json.loads(request.body.decode())
            # process attendance_data ...
            print(f"Attendance Data: {attendance_data}")
            today = datetime.now().date()
            year = attendance_data.get('year')
            section = attendance_data.get('section')
            items = attendance_data.get('items', [])
            username = user.username
            
            attendance_dict = {}
            attendance_dict={
                "year":year,
                "section":section,
                "attendance_taken_by": username,
                str(today) :{
                    "AttendanceData": items
                }
            }
            if not AttendanceRecord.objects.filter(attendance_record=attendance_dict).exists():
                AttendanceRecord.objects.create(
                    attendance_record=attendance_dict
                )
            else:
                messages.error(request, 'Attendance for today has already been submitted!')
                return JsonResponse({"success": False, "error": "Attendance for today already submitted"})
            messages.success(request, 'Attendance submitted successfully!')
            return JsonResponse({"success": True})
        except User.DoesNotExist:
            messages.error(request, 'User not found!')
            return JsonResponse({"success": False, "error": "User not found"}, status=404)
        except Exception as e:
            print(f"Error processing attendance data: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

