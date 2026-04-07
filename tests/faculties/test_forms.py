from django.test import TestCase

from faculties.forms import FacultyForm


class FacultyFormTests(TestCase):
    def test_faculty_form_valid_data(self):
        form = FacultyForm(data={
            'name': 'Engineering',
            'description': 'Engineering faculty',
            'location': 'Main building',
        })

        self.assertTrue(form.is_valid())

    def test_faculty_form_requires_name(self):
        form = FacultyForm(data={
            'name': '',
            'description': 'Engineering faculty',
            'location': 'Main building',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)