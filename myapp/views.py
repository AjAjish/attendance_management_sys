"""
=================================================================================================
                            Attendance Management System For CSE 
=================================================================================================
"""
# import Django core libs
from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
# import models
from .models import User,Student, AttendanceRecord,ManageSession
# import other libs
import json
from datetime import datetime
import csv
import pandas as pd
from io import BytesIO

"""
=================================================================================================

This Project was implemented for attendance management system using Django framework.

=================================================================================================

This attendance management system functionalities are as follows:
1. Admin Authentication: Admin can log in with their credentials. 
2. Dashboard: After logging in, users are directed to a dashboard that displays attendance records.
3. View Students: Admin can view students based on year and section.
4. Manage Students: Admin can filter and manage student records by year and section.
5. Submit Attendance: Admin can submit attendance records for students, ensuring no duplicate entries for the same date.
6. Export Attendance Data: Admin can export attendance records in CSV and Excel formats for external use.

"""

"""
Work Flow:
=================================================================================================

    The web application has folloing templates:
    1. base.html: The base template that other templates extend.
    2. home.html: The homepage template.
    3. login.html: The login page template.
    4. dashboard.html: The dashboard template displaying attendance records.
    5. student.html: The template for viewing students.
    6. manage.html: The template for managing student records.

    -->Before login user can access home , student and login page.
    -->After login user can access dashboard and manage page.

    After login() we must maintain admin id in session to access other pages.
    Handling user id :
    -->After successful login, user id is stored in session using request.session['id'].
    -->For accessing other views, user id is retrieved from session using request.session.get('id').

=================================================================================================

    To understand POST and GET request handling in Django views.

    -->POST are used to submit data to the server, such as login credentials or form submissions.
    -->GET are used to retrieve data from the server, such as loading a page or fetching records.

=================================================================================================

"""

# Create your views here.

# 1. base(request): Renders the base template.
def base(request):
    return render(request, 'base/base.html')

# 2. home(request, id=None): Renders the home template, optionally with user data if id is provided.
def home(request, id=None):
    if id:
        user = User.objects.get(id=id)
        return render(request, 'home.html', {'user': user})
    return render(request, 'home.html')

# 3. login(request): Handles user login, validates credentials, and redirects to dashboard on success.
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

# 4. dashboard(request, id=None): Displays the dashboard with attendance records for the logged-in user.
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

# 5. student(request, id=None): Displays students based on year and section filters.
def student(request, id=None):
    years = [2, 3, 4]
    section = None
    students = Student.objects.all() 

    if request.method == 'POST':
        year = request.POST.get('year')
        section = request.POST.get('section')
        print(f"Selected year{year} -- Selected section{section}")
        if year and section: 
            students = Student.objects.filter(year=year, class_section=section)
        print(students)
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


def session_management(request, id=None):

    user_id = request.session.get('id')
    user = User.objects.get(id=user_id) if user_id else None
    session = ManageSession.objects.all()
    today = datetime.now().date()
    if request.method == "POST":
        session_name = request.POST.get('session_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        edit_mode = request.POST.get('edit_mode',None)
        delete_mode = request.POST.get('delete_mode',None)

        # Debugging prints
        print(f"Session Name: {session_name}, Start Date: {start_date}, End Date: {end_date}")

        if not edit_mode and not delete_mode:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

                # Store session in Session model
                ManageSession.objects.create(
                    session_name=session_name,
                    start_date=start_date_obj,
                    end_date=end_date_obj
                )
                request.session['attendance_session_active'] = True
                request.session['session_name'] = session_name
                messages.success(request, 'Session created successfully. You can now take attendance.')
                return redirect('manage_with_id', id=id)

            except ValueError:
                messages.error(request, 'Invalid date format.')
        else:
            messages.error(request, 'Name, start date and end date are required.')
        if edit_mode:
            print("Edit mode activated")
            session_check = request.POST.get('session_name')
            try:
                session = ManageSession.objects.get(session_name=session_check)
                session.session_name = session_name
                session.start_date = start_date_obj
                session.end_date = end_date_obj
                session.save()
                messages.success(request, 'Session updated successfully.')
            except ManageSession.DoesNotExist:
                messages.error(request, 'Session not found for editing.')
            except session_check is None:
                messages.error(request, 'Session ID is required for editing.')
        if delete_mode:
            print("Delete mode activated")
            session_check = request.POST.get('session_name')
            try:
                session = ManageSession.objects.get(session_name=session_check)
                session.delete()
                request.session['attendance_session_active'] = False
                del request.session['session_name']
                messages.success(request, 'Session deleted successfully.')
            except ManageSession.DoesNotExist:
                messages.error(request, 'Session not found for deletion.')
    # Fetch the latest created session (safer than data[0])
    session = ManageSession.objects.last()

    if session:

        start_date_db = session.start_date
        end_date_db = session.end_date

        # Ensure stored values are date objects (fixes '<=' type error)
        if isinstance(start_date_db, str):
            start_date_db = datetime.strptime(start_date_db, "%Y-%m-%d").date()

        if isinstance(end_date_db, str):
            end_date_db = datetime.strptime(end_date_db, "%Y-%m-%d").date()

        print(f"DB Start Date: {start_date_db}, DB End Date: {end_date_db}, Today: {today}")

        if start_date_db > today:
            messages.warning(request, "Attendance session has not started yet.")
            return render(request, 'session.html', {'user': user, 'session': session})

        # RULE: today must be within range AND equal to end date
        if start_date_db <= today <= end_date_db or today == end_date_db:
            print("inside active session check")
            request.session['attendance_session_active'] = True
            messages.info(request, "Attendance session is ACTIVE today.")
            if today == end_date_db:
                messages.warning(request, "Today is the last day of the attendance session.")
            return render(request, 'session.html', {'user': user, 'session': session})

        else:
            print("outside active session check")
            request.session['attendance_session_active'] = False
            messages.info(request, "Attendance session is NOT active today.")
            session = None
            return render(request, 'session.html', {'user': user, 'session': session})

    return render(request, 'session.html', {'user': user, 'session': session})


# 6. manage(request, id=None): Allows admin to filter and manage student records.
def manage(request, id=None):
    years = [2, 3, 4]
    section = None
    students = None
    selected_year = None
    selected_section = None

    attendance_session_active = request.session.get('attendance_session_active')
    print(f"Attendance Session Active: {attendance_session_active}")
    
    if attendance_session_active:
        messages.info(request, "Attendance session is currently ACTIVE.")
    else:
        messages.info(request, "Attendance session is currently NOT active.")

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

    if attendance_session_active:
        messages.info(request, "Attendance session is currently ACTIVE.")
    else:
        messages.info(request, "Attendance session is currently NOT active.")

    return render(request, 'manage.html', {
        'user': user,
        'students': students,
        'years': years,
        'section': section,
        'selected_year': selected_year,
        'selected_section': selected_section,
        "attendance_session_active": attendance_session_active,
    })

# 7. logout(request): Logs out the user by clearing session data and redirects to home.
def logout(request):
    # Clear the session data
    request.session.flush()
    messages.success(request, 'Logout successful!')
    return redirect('home')

# 8. submit_attendance(request, id=None): Handles attendance submission, ensuring no duplicates for the same date.
def submit_attendance(request,id=None):
    
    today = datetime.now().date()
    if request.method == "POST":
        try:

            user = User.objects.get(id=id)
            attendance_data = json.loads(request.body.decode())
            # process attendance_data ...
            print(f"Attendance Data: {attendance_data}")
            year = attendance_data.get('year')
            section = attendance_data.get('section')
            items = attendance_data.get('items', [])
            username = user.username
            
            """
            # # Check if attendance for this date, year and section already exists
            existing_records = AttendanceRecord.objects.filter(
                attendance_record__year=year,
                attendance_record__section=section,
                attendance_record__has_key=str(today)
            ) 

            if existing_records.exists():
                messages.error(request, 'Attendance for today has already been submitted!')
                return JsonResponse({"success": False, "error": "Attendance for today already submitted"})

            """
            """
            attendance_dict structure:
            {
                "year": year,
                "section": section,
                "attendance_taken_by": username,
                "2025-09-01": {
                    "AttendanceData": [
                        {"roll": "CS101", "name": "Alice", "status": "Present"},
                        {"roll": "CS102", "name": "Bob", "status": "Absent"},
                        ...
                    ]
                }
            }
            """
            
            # if data found on same date then it will overwrite to submit .

            existing_records = AttendanceRecord.objects.filter(
                attendance_record__year=year,
                attendance_record__section=section,
                attendance_record__has_key=str(today)
            )

            if existing_records.exists():
                print("Code in existing record update block")
                existing_record = existing_records.first()
                attendance_record = existing_record.attendance_record
                attendance_record[str(today)] = {"AttendanceData": items}
                existing_record.attendance_record = attendance_record
                existing_record.save()
                messages.success(request, 'Attendance updated successfully!')
                return JsonResponse({"success": True})  

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

        
"""
I am still working on export data funactions...

"""

# 9. export_as_csv(request, id=None): Exports attendance records as a CSV file.
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

# 10. export_as_excel(request, id=None): Exports attendance records as an Excel file.
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


              