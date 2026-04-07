from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from majors.forms import MajorForm, MajorDeleteForm, MajorSearchFrom
from majors.models import Major


# Create your views here.
class MajorListView(FormMixin, ListView):
    model = Major
    context_object_name = 'list_majors'
    template_name = 'majors/list.html'
    form_class = MajorSearchFrom

    def get_queryset(self):
        queryset = super().get_queryset().annotate(total_exams=Count('exams')).select_related('faculty')
        
        form = self.get_form()
        
        if form.is_valid() and form.cleaned_data.get('query'):
            queryset = queryset.filter(name__icontains=form.cleaned_data['query'])
            
        return queryset
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = self.get_form()
        context['page_title'] = 'Majors'

        user = self.request.user
        if user.is_authenticated:
            user_majors = user.majors.all()
            context['user_majors'] = user_majors

            context['list_majors'] = context['list_majors'].exclude(id__in=user_majors.values_list('id', flat=True))

        return context


class MajorDetailView(DetailView):
    model = Major

    http_method_names = ['get']
    template_name = 'majors/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'{self.object.name} Details'
        return context


class MajorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Major
    form_class = MajorForm
    template_name = 'majors/create.html'
    success_url = reverse_lazy('majors:list')
    permission_required = ['majors.add_major']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Major'
        return context


class MajorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Major
    form_class = MajorForm
    template_name = 'majors/edit.html'
    success_url = reverse_lazy('majors:list')
    permission_required = ['majors.change_major']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit {self.object.name}'
        return context


class MajorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Major
    form_class = MajorDeleteForm
    template_name = 'majors/delete.html'
    success_url = reverse_lazy('majors:list')
    permission_required = ['majors.delete_major']

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