from django.db import models
from common.models import TimeStampModel


# Create your models here.
class ExamHall(TimeStampModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'unique': 'An exam hall with this name already exists.'
        }
    )
    capacity = models.PositiveIntegerField()
    is_computer_room = models.BooleanField(default=False)
    faculty = models.ForeignKey(
        'faculties.Faculty',
        on_delete=models.CASCADE,
        related_name='exam_halls',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}' + f' computer room' * self.is_computer_room
