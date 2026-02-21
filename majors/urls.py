from django.urls import path, include
from majors.views import majors_list, major_details

app_name = 'majors'

majors_patterns = [
]
urlpatterns = [
    path('', majors_list, name='list'),
    path('<slug:slug>/', major_details, name='details'),
]