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
        class_section=item.get("class_section "),
    )
    student.save()

print(f"Inserted {len(data)} student records successfully!")

# to store json data on model 
# open shell and enter----> exec(open('data.py').read())

