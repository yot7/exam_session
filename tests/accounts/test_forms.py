from django.test import TestCase

from accounts.forms import RegistrationForm
from faculties.models import Faculty
from majors.models import Major


class RegistrationFormTests(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Engineering',
            description='Engineering faculty',
            location='Main building',
        )
        self.major = Major.objects.create(
            name='Computer Science',
            description='CS major',
            faculty=self.faculty,
        )

    def test_registration_form_valid_data(self):
        form = RegistrationForm(data={
            'email': 'student@example.com',
            'username': 'student1',
            'first_name': 'John',
            'last_name': 'Doe',
            'majors': [self.major.pk],
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid())

    def test_registration_form_assigns_student_group_on_save(self):
        form = RegistrationForm(data={
            'email': 'student@example.com',
            'username': 'student1',
            'first_name': 'John',
            'last_name': 'Doe',
            'majors': [self.major.pk],
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertTrue(user.groups.filter(name='Student').exists())
        self.assertTrue(user.majors.filter(pk=self.major.pk).exists())

    def test_major_field_labels_use_major_name(self):
        field = RegistrationForm().fields['majors']
        label = field.label_from_instance(self.major)

        self.assertEqual(label, self.major.name)