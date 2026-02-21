from django.contrib import admin

from exams.models import Exam


# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    ...