from django.db import models
from common.models import TimeStampModel


# Create your models here.
class ExamHall(TimeStampModel):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_computer_room = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}' + f' computer room' * self.is_computer_room
