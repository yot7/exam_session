from django.urls import path, include
from exam_halls.views import exam_hall_delete, exam_hall_delete_error, \
    ExamHallListView, ExamHallDetailView, ExamHallCreateView, ExamHallUpdateView

app_name = 'exam_halls'

exam_halls_patterns = [
    path('', ExamHallDetailView.as_view(), name='details'),
    path('edit/', ExamHallUpdateView.as_view(), name='edit'),
    path('delete/', exam_hall_delete, name='delete'),
]
urlpatterns = [
    path('', ExamHallListView.as_view(), name='list'),
    path('create/', ExamHallCreateView.as_view(), name='create'),
    path('delete_error/', exam_hall_delete_error, name='delete_error'),
    path('<int:pk>/', include(exam_halls_patterns))
]
