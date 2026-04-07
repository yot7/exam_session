from django.test import TestCase

from faculties.models import Faculty
from majors.forms import MajorForm


class MajorFormTests(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Engineering',
            description='Engineering faculty',
            location='Main building',
        )

    def test_major_form_valid_data(self):
        form = MajorForm(data={
            'name': 'Computer Science',
            'description': 'CS major',
            'faculty': self.faculty.pk,
        })

        self.assertTrue(form.is_valid())

    def test_major_form_requires_faculty(self):
        form = MajorForm(data={
            'name': 'Computer Science',
            'description': 'CS major',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('faculty', form.errors)