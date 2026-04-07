from django.test import TestCase

from exams.models import Exam
from faculties.models import Faculty
from majors.models import Major
from exams.forms import PrepExamFormBasic


class ExamFormTests(TestCase):
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

    def test_exam_prep_form_valid_data(self):
        form = PrepExamFormBasic(data={
            'subject': 'Math',
            'major': self.major.pk,
            'needs_computers': False,
            'number_of_examinees': 30,
            'date': '2026-05-01',
            'start_time': '10:00',
            'end_time': '11:00',
        })

        self.assertTrue(form.is_valid())

    def test_exam_prep_form_rejects_short_exam(self):
        form = PrepExamFormBasic(data={
            'subject': 'Math',
            'major': self.major.pk,
            'needs_computers': False,
            'number_of_examinees': 30,
            'date': '2026-05-01',
            'start_time': '10:00',
            'end_time': '10:00',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('end_time', form.errors)

    def test_exam_form_rejects_duplicate_subject_and_major(self):
        Exam.objects.create(
            subject='Math',
            major=self.major,
            needs_computers=False,
            number_of_examinees=30,
            date='2026-05-01',
            start_time='10:00',
            end_time='11:00',
        )

        form = PrepExamFormBasic(data={
            'subject': 'Math',
            'major': self.major.pk,
            'needs_computers': False,
            'number_of_examinees': 30,
            'date': '2026-05-02',
            'start_time': '10:00',
            'end_time': '11:00',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_exam_form_rejects_same_start_and_end_time(self):
        form = PrepExamFormBasic(data={
            'subject': 'Physics',
            'major': self.major.pk,
            'needs_computers': False,
            'number_of_examinees': 30,
            'date': '2026-05-02',
            'start_time': '10:00',
            'end_time': '10:00',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('end_time', form.errors)