from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User,Student, AttendanceRecord
import json
from datetime import datetime
from django.http import JsonResponse,HttpResponse
import csv
import pandas as pd
from io import BytesIO


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
                # Make it userid on session after login
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
    id = request.session.get('id')
    if id:
        user = User.objects.get(id=id)
        records_qs = AttendanceRecord.objects.all()
        # Ensure we pass dict objects, not None or empty string
        records = []
        for rec in records_qs:
            if rec.attendance_record:
                records.append(rec.attendance_record)
        # If you want to filter by id, you can do:
        # if id is not None:
        #     records = [rec.attendance_record for rec in records_qs if rec.id == id]
        return render(request, "dashboard.html", {"user": user, "records": records})
    return render(request, 'dashboard.html', {"user": None, "records": []})

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
            'years': years,
            'section': section,
        })

    # GET Request – just load the page with years and user
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id) if user_id else None

    return render(request, 'student.html', {
        'user': user,
        'students': students,
        'years': years,
        'section': section,
    })

def manage(request, id=None):
    years = [2, 3, 4]
    students = None

    if request.method == 'POST':
        # Extract year and section for filtering
        year = request.POST.get('year')
        section = request.POST.get('section')
        print(f"Filtering students for Year: {year}, Section: {section}")
        selected_year = year
        selected_section = section

        # After filtering, fetch students for UI display
        if year and section:
            students = Student.objects.filter(year=year, class_section=section)

    # Get user from session for rendering
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id) if user_id else None

    return render(request, 'manage.html', {
        'user': user,
        'students': students,
        'years': years,
        'section': section,
        'selected_year': selected_year,
        'selected_section': selected_section
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
            
            # Check if attendance for this date, year and section already exists
            existing_records = AttendanceRecord.objects.filter(
                attendance_record__year=year,
                attendance_record__section=section,
                attendance_record__has_key=str(today)
            ) 

            if existing_records.exists():
                messages.error(request, 'Attendance for today has already been submitted!')
                return JsonResponse({"success": False, "error": "Attendance for today already submitted"})

            attendance_dict = {}
            attendance_dict={
                "year":year,
                "section":section,
                "attendance_taken_by": username,
                str(today) :{
                    "AttendanceData": items
                }
            }
            
            AttendanceRecord.objects.create(attendance_record=attendance_dict)

            messages.success(request, 'Attendance submitted successfully!')
            return JsonResponse({"success": True})
        except User.DoesNotExist:
            messages.error(request, 'User not found!')
            return JsonResponse({"success": False, "error": "User not found"}, status=404)
        except Exception as e:
            print(f"Error processing attendance data: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def export_as_csv(request, id=None):
    if id is None:
        return JsonResponse({"success": False, "error": "Invalid ID"}, status=400)

    try:
        records = AttendanceRecord.objects.all()
    except AttendanceRecord.DoesNotExist:
        return JsonResponse({"success": False, "error": "No records found"}, status=404)

    if not records.exists():
        return JsonResponse({"success": False, "error": "No records found"}, status=404)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Status'])

    try:
        for record in records:
            # Assuming attendance_record is a dict like {'2025-09-01': 'Present'}
            for date, status in record.attendance_record.items():
                writer.writerow([date, status])
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

    return response

def export_as_excel(request, id=None):
    if id is None:
        return JsonResponse({"success": False, "error": "Invalid ID"}, status=400)

    try:
        data = AttendanceRecord.objects.all().values()
    except AttendanceRecord.DoesNotExist:
        return JsonResponse({"success": False, "error": "No records found"}, status=404)

    if not data.exists():
        return JsonResponse({"success": False, "error": "No records found"}, status=404)

    records = []
    for entry in data:
        record = entry['attendance_record']
        year = record['year']
        section = record['section']
        taken = record['attendance_taken_by']

        for key, value in record.items():
            if key in ['year', 'section', 'attendance_taken_by']:
                continue
            if isinstance(value, dict) and 'AttendanceData' in value:
                date = key
                for student in value['AttendanceData']:
                    records.append({
                        'Year': year,
                        'Section': section,
                        'Date': date,
                        'Roll': student['roll'],
                        'Name': student['name'],
                        'Status': student['status'],
                        'Taken By': taken
                    })

    # Convert to DataFrame
    df = pd.DataFrame(records)
    # Write to an in-memory buffer
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')

    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    print(f"HttpResponse: {response}")
    response['Content-Disposition'] = 'attachment; filename="attendance_data.xlsx"'
    print(f"response after setting header: {response}")
    return response