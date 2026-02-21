from django.urls import path
from exams.views import exams_list, exam_details

app_name = 'exams'

urlpatterns = [
    path('', exams_list, name='list'),
    path('<int:pk>/', exam_details, name='details')
]