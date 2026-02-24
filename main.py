import os
import django
from datetime import date, time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_session.settings')
django.setup()

from majors.models import Major
from exam_halls.models import ExamHall
from exams.models import Exam

def populate_data():
    print("Populating data...")

    # Create Majors
    major1, _ = Major.objects.get_or_create(name="Computer Science")
    major2, _ = Major.objects.get_or_create(name="Mathematics")
    major3, _ = Major.objects.get_or_create(name="Physics")
    print(f"Created majors: {major1}, {major2}, {major3}")

    # Create Exam Halls
    hall1, _ = ExamHall.objects.get_or_create(
        name="Hall A",
        defaults={'capacity': 50, 'is_computer_room': False}
    )
    hall2, _ = ExamHall.objects.get_or_create(
        name="Lab 1",
        defaults={'capacity': 30, 'is_computer_room': True}
    )
    hall3, _ = ExamHall.objects.get_or_create(
        name="Hall B",
        defaults={'capacity': 100, 'is_computer_room': False}
    )
    print(f"Created halls: {hall1}, {hall2}, {hall3}")

    # Create Exams
    # Exam 1: CS Exam in Lab 1 (needs computers)
    exam1, created1 = Exam.objects.get_or_create(
        subject="Intro to Programming",
        major=major1,
        defaults={
            'needs_computers': True,
            'number_of_examinees': 25,
            'date': date(2024, 6, 15),
            'start_time': time(9, 0),
            'end_time': time(12, 0),
        }
    )
    if created1:
        exam1.exam_halls.add(hall2)
        print(f"Created exam: {exam1}")
    else:
        print(f"Exam {exam1} already exists")

    # Exam 2: Math Exam in Hall A
    exam2, created2 = Exam.objects.get_or_create(
        subject="Calculus I",
        major=major2,
        defaults={
            'needs_computers': False,
            'number_of_examinees': 45,
            'date': date(2024, 6, 16),
            'start_time': time(14, 0),
            'end_time': time(17, 0),
        }
    )
    if created2:
        exam2.exam_halls.add(hall1)
        print(f"Created exam: {exam2}")
    else:
        print(f"Exam {exam2} already exists")

    # Exam 3: Physics Exam in Hall B
    exam3, created3 = Exam.objects.get_or_create(
        subject="Mechanics",
        major=major3,
        defaults={
            'needs_computers': False,
            'number_of_examinees': 80,
            'date': date(2024, 6, 17),
            'start_time': time(10, 0),
            'end_time': time(13, 0),
        }
    )
    if created3:
        exam3.exam_halls.add(hall3)
        print(f"Created exam: {exam3}")
    else:
        print(f"Exam {exam3} already exists")

    print("Data population complete.")

if __name__ == '__main__':
    populate_data()