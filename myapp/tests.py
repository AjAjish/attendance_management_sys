from django.test import TestCase
from .models import Student, User, AttendanceRecord, ManageSession


session = ManageSession.objects.all()

# to print session all columns
for session in session:
    print(session.session_name)
    print(session.start_date)
    print(session.end_date)

# Create your tests here.
