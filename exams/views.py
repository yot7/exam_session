from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, ListView
from formtools.wizard.views import SessionWizardView

from exams.forms import ExamSearchForm, PrepExamFormCreate, ExamFormCreate, PrepExamFormEdit, ExamFormEdit, \
    ExamDeleteForm
from exams.models import Exam


# Create your views here.
class ExamListView(ListView, FormView):
    model = Exam
    context_object_name = 'list_exams'
    template_name = 'exams/list.html'
    form_class = ExamSearchForm

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'query' in self.request.GET:
            queryset = queryset.filter(subject__icontains=self.request.GET['query'])

        if 'date' in self.request.GET and self.request.GET['date'] != '':
            queryset = queryset.filter(date=self.request.GET['date'])

        return queryset


def exam_details(request: HttpRequest, pk: int) -> HttpResponse:
    searched_exam = get_object_or_404(
        Exam.objects.prefetch_related('exam_halls'),
        pk=pk,
    )

    context = {
        'searched_exam': searched_exam,
        'page_title': f'{searched_exam.subject} - {searched_exam.major.name if searched_exam.major else "Major N/A"} Details'
    }

    return render(request, 'exams/details.html', context)


class ExamCreateWizard(SessionWizardView):
    form_list = [PrepExamFormCreate, ExamFormCreate]
    template_name = 'exams/create_wizard.html'

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == '1':
            step0_data = self.get_cleaned_data_for_step('0')
            kwargs.update({'step0_data': step0_data})

        return kwargs

    def done(self, form_list, **kwargs):
        step1_data = form_list[0].cleaned_data
        step2_data = form_list[1].cleaned_data

        new_exam = Exam.objects.create(
            subject=step1_data['subject'],
            major=step1_data['major'],
            needs_computers=step1_data['needs_computers'],
            number_of_examinees=step1_data['number_of_examinees'],
            date=step1_data['date'],
            start_time=step1_data['start_time'],
            end_time=step1_data['end_time'],
        )
        new_exam.exam_halls.set(step2_data['exam_halls'])
        new_exam.save()

        return redirect('exams:list')

class ExamEditWizard(SessionWizardView):
    form_list = [PrepExamFormEdit, ExamFormEdit]
    template_name = 'exams/edit_wizard.html'

    def get_form_initial(self, step):
        pk = self.kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)

        if step == '0':
            return {
                'subject': exam.subject,
                'major': exam.major,
                'needs_computers': exam.needs_computers,
                'number_of_examinees': exam.number_of_examinees,
                'date': exam.date,
                'start_time': exam.start_time,
                'end_time': exam.end_time,
                'exam_pk': pk,
            }
        elif step == '1':
            return {
                'exam_halls': exam.exam_halls.all(),
                'exam_pk': pk,
            }

        return super().get_form_initial(step)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == '1':
            step0_data = self.get_cleaned_data_for_step('0')
            kwargs.update({'step0_data': step0_data})

        return kwargs

    def done(self, form_list, **kwargs):
        step1_data = form_list[0].cleaned_data
        step2_data = form_list[1].cleaned_data
        pk = self.kwargs['pk']
        exam = get_object_or_404(Exam, pk=pk)

        exam.subject = step1_data['subject']
        exam.major = step1_data['major']
        exam.needs_computers = step1_data['needs_computers']
        exam.number_of_examinees = step1_data['number_of_examinees']
        exam.date = step1_data['date']
        exam.start_time = step1_data['start_time']
        exam.end_time = step1_data['end_time']
        exam.save()

        exam.exam_halls.set(step2_data['exam_halls'])

        return redirect('exams:details', pk)


def exam_hall_delete(request: HttpRequest, pk: int):
    searched_exam = get_object_or_404(Exam, pk=pk)
    form = ExamDeleteForm(request.POST or None, instance=searched_exam)

    if request.method == 'POST' and form.is_valid():
        searched_exam.exam_halls.clear()
        searched_exam.delete()
        return redirect('exams:list')

    context = {
        'form': form,
        'page_title': f'Delete {searched_exam.subject} - {searched_exam.major.name}'
    }

    return render(request, 'exams/delete.html', context)
