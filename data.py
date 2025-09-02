import json
from myapp.models import Student

# Load data from students.json
with open('data.json', 'r') as f:
    data = json.load(f)

for item in data:
    student = Student(
        name=item.get("name"),
        roll_number=item.get("roll_number"),
        course=item.get("course", "BE Computer Science and Engineering"),
        year=item.get("year"),
        class_section=item.get("class_section"),
    )
    student.save()

print(f"Inserted {len(data)} student records successfully!")

# to store json data on model 
# open shell and enter----> exec(open('demo.py').read())


def sut_attendance(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        body = request.body.decode() if request.body else ""
        if not body:
            return JsonResponse({"success": False, "error": "Empty payload"}, status=400)

        data = json.loads(body)

        # Support two payload shapes:
        # 1) { items: [ { roll, name, status }, ... ], year, section, date }
        # 2) { roll_or_student_id: status, ... } (legacy)

        today = datetime.now().date()
        processed = 0
        errors = []

        if isinstance(data, dict) and "items" in data:
            year = data.get("year")
            section = data.get("section")
            date_str = data.get("date")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str).date()
                except Exception:
                    date = today
            else:
                date = today

            items = data.get("items", []) or []
            for item in items:
                roll = item.get("roll")
                status = item.get("status")
                if roll is None or status is None:
                    errors.append({"item": item, "error": "missing roll or status"})
                    continue

                roll_str = str(roll)
                student = Student.objects.filter(roll_number=roll_str)
                if year:
                    student = student.filter(year=year)
                if section:
                    student = student.filter(class_section=section)
                student = student.first()

                if not student:
                    errors.append({"roll": roll_str, "error": "student not found"})
                    continue

                record_obj, created = AttendanceRecord.objects.get_or_create(student=student, date=date)
                record_obj.attendance_record = {"status": status}
                record_obj.save()
                processed += 1

        elif isinstance(data, dict):
            # legacy mapping: keys are ids or roll numbers
            for key, status in data.items():
                # skip non-data keys
                if key in ("date", "year", "section"):
                    continue
                # try as numeric id first
                student = None
                try:
                    student = Student.objects.filter(id=int(key)).first()
                except Exception:
                    student = None

                if not student:
                    # try roll match
                    student = Student.objects.filter(roll_number=str(key)).first()

                if not student:
                    errors.append({"key": key, "error": "student not found"})
                    continue

                record_obj, created = AttendanceRecord.objects.get_or_create(student=student, date=today)
                record_obj.attendance_record = {"status": status}
                record_obj.save()
                processed += 1

        else:
            return JsonResponse({"success": False, "error": "Unsupported payload format"}, status=400)

        return JsonResponse({"success": True, "processed": processed, "errors": errors})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error processing attendance data: {e}")