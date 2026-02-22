from django.urls import path, include
from exam_halls.views import exam_hall_details, exam_halls_list, exam_hall_create, exam_hall_edit, exam_hall_delete

app_name = 'exam_halls'

exam_halls_patterns = [
    path('', exam_hall_details, name='details'),
    path('edit/', exam_hall_edit, name='edit'),
    path('delete/', exam_hall_delete, name='delete'),
]
urlpatterns = [
    path('', exam_halls_list, name='list'),
    path('create/', exam_hall_create, name='create'),
    path('<int:pk>/', include(exam_halls_patterns))
]
