from django.db import models
from common.models import TimeStampModel


# Create your models here.
class Exam(TimeStampModel):
    subject = models.CharField(max_length=50)
    major = models.ForeignKey(
        'majors.Major',
        on_delete=models.CASCADE,
        related_name='exams',
        null=True,
        blank=True
    )
    needs_computers = models.BooleanField(default=False)
    number_of_examinees = models.PositiveIntegerField()
    exam_halls = models.ManyToManyField(
        'exam_halls.ExamHall',
        related_name='hosted_exams'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date']
        unique_together = ['subject', 'major']

    def __str__(self):
        return f'{self.subject}'