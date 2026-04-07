from django.urls import path, include
from majors.views import MajorListView, MajorDetailView, MajorCreateView, MajorUpdateView, MajorDeleteView

app_name = 'majors'

majors_patterns = [
    path('', MajorDetailView.as_view(), name='details'),
    path('edit/', MajorUpdateView.as_view(), name='edit'),
    path('delete/', MajorDeleteView.as_view(), name='delete'),
]
urlpatterns = [
    path('', MajorListView.as_view(), name='list'),
    path('create/', MajorCreateView.as_view(), name='create'),
    path('<slug:slug>/', include(majors_patterns)),
]