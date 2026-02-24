from django import template
from django.db.models import QuerySet, Sum

from exam_halls.models import ExamHall

register = template.Library()

@register.simple_tag
def sum_capacity(exam_halls: QuerySet[ExamHall]):
    return exam_halls.aggregate(Sum('capacity'))['capacity__sum'] or 0