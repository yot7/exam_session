from django.urls import path, include
from exams.views import ExamListView, ExamCreateWizard, ExamEditWizard, ExamDetailView, ExamDeleteView

app_name = 'exams'

exam_patterns = [
    path('', ExamDetailView.as_view(), name='details'),
    path('edit/', ExamEditWizard.as_view(), name='edit'),
    path('delete/', ExamDeleteView.as_view(), name='delete'),
]

urlpatterns = [
    path('', ExamListView.as_view(), name='list'),
    path('create/', ExamCreateWizard.as_view(), name='create'),
    path('<int:pk>/', include(exam_patterns)),
]