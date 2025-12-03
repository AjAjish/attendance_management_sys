from django.db import models
import uuid

class Student(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    roll_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    course = models.CharField(default="BE Computer Science and Engineering",max_length=50)
    year = models.IntegerField(null=True, blank=True)
    class_section = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number}) - {self.class_section}, Year {self.year}, Course: {self.course}"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(default="staff", max_length=10)

    def __str__(self):
        return f"{self.id} - {self.username} ({self.email}) - {self.password}"

class AttendanceRecord(models.Model):
    attendance_record = models.JSONField(default=dict, blank=True)

class ManageSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.session_name} ({self.start_date} to {self.end_date})"
