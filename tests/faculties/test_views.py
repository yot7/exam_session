from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from faculties.models import Faculty

User = get_user_model()


class FacultyViewsTests(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Engineering',
            description='Engineering faculty',
            location='Main building',
        )

        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin1',
            password='StrongPass123!',
            last_name='Admin',
        )

    def test_faculty_list_page_loads(self):
        response = self.client.get(reverse('faculties:list'))
        self.assertEqual(response.status_code, 200)

    def test_faculty_detail_page_loads(self):
        response = self.client.get(reverse('faculties:details', kwargs={'slug': self.faculty.slug}))
        self.assertEqual(response.status_code, 200)

    def test_faculty_create_page_requires_login(self):
        response = self.client.get(reverse('faculties:create'))
        self.assertEqual(response.status_code, 302)