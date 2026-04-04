from django.shortcuts import render
from django.views.generic import ListView

from faculties.models import Faculty


# Create your views here.
class FacultyListView(ListView):
    model = Faculty
    context_object_name = 'list_faculties'
    template_name = 'faculties/list.html'