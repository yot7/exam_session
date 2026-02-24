from django.urls import path, include
from exams.views import exam_details, ExamListView, ExamCreateWizard, ExamEditWizard, exam_hall_delete

app_name = 'exams'

exam_patterns = [
    path('', exam_details, name='details'),
    path('edit/', ExamEditWizard.as_view(), name='edit'),
    path('delete/', exam_hall_delete, name='delete'),
]

urlpatterns = [
    path('', ExamListView.as_view(), name='list'),
    path('create/', ExamCreateWizard.as_view(), name='create'),
    path('<int:pk>/', include(exam_patterns)),
]