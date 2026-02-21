from django.contrib import admin

from majors.models import Major


# Register your models here.
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    ...