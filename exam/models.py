from django.db import models

# Create your models here.
class Exam(models.Model):
    subject = models.CharField(max_length=50)
    needs_computers = models.BooleanField(default=False)
    number_of_examinees = models.PositiveIntegerField()
    exam_hall = models.ManyToManyField(
        'exam_hall.ExamHall',
        related_name='hosted_exams'
    )
    date = models.DateField(
        # TODO: Validation
    )
    start_time = models.TimeField(
        # TODO: Validation
    )
    end_time = models.TimeField(
        # TODO: Validation
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.subject}'