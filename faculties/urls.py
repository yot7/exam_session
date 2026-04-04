from django.urls import path

from faculties.views import FacultyListView

app_name = 'faculties'

urlpatterns = [
    path('', FacultyListView.as_view(), name='list'),
]