import os
import django
from datetime import date, time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_session.settings')
django.setup()

from faculties.models import Faculty
from majors.models import Major
from exam_halls.models import ExamHall
from exams.models import Exam

def populate_data():
    print("Clearing existing data...")
    Exam.objects.all().delete()
    ExamHall.objects.all().delete()
    Major.objects.all().delete()
    Faculty.objects.all().delete()

    print("Populating data...")

    # Create Faculty
    fmi = Faculty.objects.create(
        name="Mathematics and Informatics",
        location="James Bourchier Blvd 5, Sofia"
    )
    print(f"Created faculty: {fmi}")

    # Create Majors
    major1 = Major.objects.create(name="Computer Science", faculty=fmi)
    major2 = Major.objects.create(name="Mathematics", faculty=fmi)
    major3 = Major.objects.create(name="Data Analysis", faculty=fmi)
    print(f"Created majors: {major1}, {major2}, {major3}")

    # Create Exam Halls
    hall1 = ExamHall.objects.create(
        name="Hall A",
        capacity=50,
        is_computer_room=False,
        faculty=fmi,
    )
    hall2 = ExamHall.objects.create(
        name="Lab 1",
        capacity=30,
        is_computer_room=True,
        faculty=fmi,
    )
    hall3 = ExamHall.objects.create(
        name="Hall B",
        capacity=100,
        is_computer_room=False,
        faculty=fmi,
    )
    print(f"Created halls: {hall1}, {hall2}, {hall3}")

    # Create Exams
    # Exam 1: CS Exam in Lab 1 (needs computers)
    exam1 = Exam.objects.create(
        subject="Intro to Programming",
        major=major1,
        needs_computers=True,
        number_of_examinees=25,
        date=date(2024, 6, 15),
        start_time=time(9, 0),
        end_time=time(12, 0),
    )
    exam1.exam_halls.add(hall2)
    print(f"Created exam: {exam1}")

    # Exam 2: Math Exam in Hall A
    exam2 = Exam.objects.create(
        subject="Calculus I",
        major=major2,
        needs_computers=False,
        number_of_examinees=45,
        date=date(2024, 6, 16),
        start_time=time(14, 0),
        end_time=time(17, 0),
    )
    exam2.exam_halls.add(hall1)
    print(f"Created exam: {exam2}")

    # Exam 3: Physics Exam in Hall B
    exam3 = Exam.objects.create(
        subject="Linear Algebra",
        major=major3,
        needs_computers=False,
        number_of_examinees=80,
        date=date(2024, 6, 17),
        start_time=time(10, 0),
        end_time=time(13, 0),
    )
    exam3.exam_halls.add(hall3)
    print(f"Created exam: {exam3}")

    print("Data population complete.")

if __name__ == '__main__':
    populate_data()