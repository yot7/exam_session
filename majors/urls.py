from django.urls import path, include
from majors.views import majors_list, major_details, major_create, major_edit, major_delete

app_name = 'majors'

majors_patterns = [
    path('edit/', major_edit, name='edit'),
    path('delete/', major_delete, name='delete'),
]
urlpatterns = [
    path('', majors_list, name='list'),
    path('create/', major_create, name='create'),
    path('<int:pk>/', include(majors_patterns)),
    path('<slug:slug>/', major_details, name='details'),
]