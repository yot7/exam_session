from django.urls import path
from exam_halls.views import exam_hall_details, exam_halls_list

app_name = 'exam_halls'

urlpatterns = [
    path('', exam_halls_list, name='list'),
    path('<int:pk>/', exam_hall_details, name='details')
]
