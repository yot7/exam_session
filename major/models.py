from django.db import models

# Create your models here.
class Major(models.Model):
    name = models.CharField(max_length=50)
    exams = models.ForeignKey(
        'exam.Exam',
        on_delete=models.CASCADE,
        related_name='major'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name