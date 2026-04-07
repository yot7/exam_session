from django.urls import path, include

from faculties.views import FacultyListView, FacultyCreateView, FacultyDetailView, FacultyUpdateView, FacultyDeleteView

app_name = 'faculties'

faculties_patterns = [
    path('', FacultyDetailView.as_view(), name='details'),
    path('edit/', FacultyUpdateView.as_view(), name='edit'),
    path('delete/', FacultyDeleteView.as_view(), name='delete'),
]
urlpatterns = [
    path('', FacultyListView.as_view(), name='list'),
    path('create/', FacultyCreateView.as_view(), name='create'),
    path('<slug:slug>/', include(faculties_patterns)),
]