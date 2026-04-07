from django.test import TestCase

from exam_halls.forms import ExamHallFormBasic
from faculties.models import Faculty
from exam_halls.models import ExamHall


class ExamHallFormTests(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Engineering',
            description='Engineering faculty',
            location='Main building',
        )

    def test_exam_hall_form_accepts_valid_capacity(self):
        form = ExamHallFormBasic(data={
            'name': 'Room 101',
            'capacity': 50,
            'is_computer_room': False,
            'faculty': self.faculty.pk,
        })

        self.assertTrue(form.is_valid())

    def test_exam_hall_form_rejects_duplicate_name_in_same_faculty(self):
        ExamHall.objects.create(
            name='Room 101',
            capacity=50,
            is_computer_room=False,
            faculty=self.faculty,
        )

        form = ExamHallFormBasic(data={
            'name': 'Room 101',
            'capacity': 60,
            'is_computer_room': True,
            'faculty': self.faculty.pk,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)