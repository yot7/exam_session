from datetime import time

from django.core.exceptions import ValidationError


def validate_start_time(value):
    if not time(8) <= value <= time(19):
        raise ValidationError('Start time must be between 8:00 and 19:00')
    if value.minute != 0:
        raise ValidationError('Minutes must be 0')

def validate_end_time(value):
    if value > time(20):
        raise ValidationError('Exam must be completed by 20:00')
    if value.minute != 0:
        raise ValidationError('Minutes must be 0')
