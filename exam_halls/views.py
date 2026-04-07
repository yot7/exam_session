from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from exam_halls.forms import ExamHallCreateForm, ExamHallEditForm, ExamHallDeleteForm, ExamHallSearchFrom
from exam_halls.models import ExamHall


# Create your views here.
class ExamHallListView(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, ListView):
    model = ExamHall
    context_object_name = 'list_exam_halls'
    template_name = 'exam_halls/list.html'
    form_class = ExamHallSearchFrom
    permission_required = ['exam_halls.view_examhall']

    def get_queryset(self):
        queryset = super().get_queryset()

        form = self.get_form()

        if form.is_valid():
            if form.cleaned_data['is_computer_room']:
                queryset = queryset.filter(is_computer_room=True)

            if form.cleaned_data.get('query'):
                queryset = queryset.filter(
                    Q(name__icontains=form.cleaned_data['query'])
                )

            if form.cleaned_data.get('min_capacity'):
                queryset = queryset.filter(
                    Q(capacity__gte=form.cleaned_data['min_capacity'])
                )

        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = self.get_form()
        context['page_title'] = 'Exam Halls'
        return context


class ExamHallDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ExamHall

    http_method_names = ['get']
    template_name = 'exam_halls/details.html'
    permission_required = ['exam_halls.view_examhall']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'{self.object.name} Details'
        return context


class ExamHallCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExamHall
    form_class = ExamHallCreateForm
    template_name = 'exam_halls/create.html'
    success_url = reverse_lazy('exam_halls:list')
    permission_required = ['exam_halls.add_examhall']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Exam Hall'
        return context


class ExamHallUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExamHall
    form_class = ExamHallEditForm
    template_name = 'exam_halls/edit.html'
    success_url = reverse_lazy('exam_halls:list')
    permission_required = ['exam_halls.change_examhall']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit {self.object.name}'
        return context


@login_required
@permission_required('exam_halls.delete_examhall')
def exam_hall_delete_error(request: HttpRequest) -> HttpResponse:
    context = {
        'page_title': 'Delete Error'
    }
    return render(request, 'exam_halls/delete_error.html', context)


@login_required
@permission_required('exam_halls.delete_examhall')
def exam_hall_delete(request: HttpRequest, pk: int) -> HttpResponse:
    searched_exam_hall = get_object_or_404(ExamHall, pk=pk)
    form = ExamHallDeleteForm(request.POST or None, instance=searched_exam_hall)

    if request.method == 'POST' and form.is_valid():
        if searched_exam_hall.hosted_exams.exists():
            return redirect('exam_halls:delete_error')

        searched_exam_hall.delete()
        return redirect('exam_halls:list')

    context = {
        'form': form,
        'page_title': f'Delete {searched_exam_hall.name}'
    }

    return render(request, 'exam_halls/delete.html', context)
