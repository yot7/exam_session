from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from faculties.forms import FacultyForm, FacultyDeleteForm
from faculties.models import Faculty
from exams.models import Exam
from exam_halls.models import ExamHall


# Create your views here.
class FacultyListView(ListView):
    model = Faculty
    context_object_name = 'list_faculties'
    template_name = 'faculties/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        user_faculties = None
        if user.is_authenticated and user.majors.exists():
            user_faculties = Faculty.objects.filter(majors__users=user).distinct()
            context['user_faculties'] = user_faculties
            context['list_faculties'] = context['list_faculties'].exclude(id__in=user_faculties.values_list('id', flat=True))
            
        return context


class FacultyDetailView(DetailView):
    model = Faculty

    http_method_names = ['get']
    template_name = 'faculties/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        faculty = self.object

        faculty_majors = faculty.majors.all()

        faculty_exams = Exam.objects.filter(major__faculty=faculty)

        total_majors = faculty_majors.count()
        
        total_exam_halls = ExamHall.objects.filter(faculty=faculty).distinct().count()

        last_added_major = faculty_majors.order_by('-created_at').first()
        last_added_exam = faculty_exams.order_by('-created_at').first()

        context['page_title'] = f'{faculty.name} Details'
        context['total_majors'] = total_majors
        context['total_exam_halls'] = total_exam_halls
        context['last_added_major'] = last_added_major
        context['last_added_exam'] = last_added_exam
        return context


class FacultyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'faculties/create.html'
    success_url = reverse_lazy('faculties:list')
    permission_required = ['faculties.add_faculty']



class FacultyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'faculties/edit.html'
    success_url = reverse_lazy('faculties:list')
    permission_required = ['faculties.change_faculty']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit {self.object.name}'
        return context


class FacultyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Faculty
    form_class = FacultyDeleteForm
    template_name = 'faculties/delete.html'
    success_url = reverse_lazy('faculties:list')
    permission_required = ['faculties.delete_faculty']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Delete {self.object.name}'
        if 'form' not in context:
            context['form'] = self.get_form()
        return context
