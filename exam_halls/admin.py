from django.contrib import admin

from exam_halls.models import ExamHall


# Register your models here.
@admin.register(ExamHall)
class ExamHallAdmin(admin.ModelAdmin):
    ...