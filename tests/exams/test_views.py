from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from faculties.models import Faculty
from majors.models import Major
from exams.models import Exam

User = get_user_model()


class ExamViewsTests(TestCase):
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
        self.exam = Exam.objects.create(
            subject='Math',
            major=self.major,
            needs_computers=False,
            number_of_examinees=30,
            date='2026-05-01',
            start_time='10:00',
            end_time='11:00',
        )
        self.user = User.objects.create_user(
            email='viewer@example.com',
            username='viewer1',
            password='StrongPass123!',
            last_name='Viewer',
        )

    def test_exam_list_requires_login(self):
        response = self.client.get(reverse('exams:list'))
        self.assertEqual(response.status_code, 302)

    def test_exam_detail_requires_login(self):
        response = self.client.get(reverse('exams:details', kwargs={'pk': self.exam.pk}))
        self.assertEqual(response.status_code, 302)