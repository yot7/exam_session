from django.test import TestCase
from django.urls import reverse

from faculties.models import Faculty
from majors.models import Major


class MajorViewsTests(TestCase):
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

    def test_major_list_page_loads(self):
        response = self.client.get(reverse('majors:list'))
        self.assertEqual(response.status_code, 200)

    def test_major_detail_page_loads(self):
        response = self.client.get(reverse('majors:details', kwargs={'slug': self.major.slug}))
        self.assertEqual(response.status_code, 200)

    def test_major_create_page_requires_login(self):
        response = self.client.get(reverse('majors:create'))
        self.assertEqual(response.status_code, 302)