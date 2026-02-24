from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from exam_halls.forms import ExamHallCreateForm, ExamHallEditForm, ExamHallDeleteForm, ExamHallSearchFrom
from exam_halls.models import ExamHall


# Create your views here.
def exam_halls_list(request: HttpRequest) -> HttpResponse:
    search_form = ExamHallSearchFrom(request.GET or None)

    list_exam_halls = ExamHall.objects.all()

    if 'query' in request.GET:
        if search_form.is_valid():
            if search_form.cleaned_data['is_computer_room']:
                list_exam_halls = list_exam_halls.filter(is_computer_room=True)

            list_exam_halls = list_exam_halls.filter(
                Q(name__icontains=search_form.cleaned_data['query'])
                &
                Q(capacity__gte=search_form.cleaned_data['min_capacity'])
            )

    context = {
        'list_exam_halls': list_exam_halls,
        'page_title': 'Exam Halls',
        'search_form': search_form
    }

    return render(request, 'exam_halls/list.html', context)

def exam_hall_details(request: HttpRequest, pk: int) -> HttpResponse:
    searched_exam_hall = get_object_or_404(
        ExamHall.objects.prefetch_related('hosted_exams'),
        pk=pk,
    )

    context = {
        'searched_exam_hall': searched_exam_hall,
        'page_title': f'{searched_exam_hall.name} Details'
    }

    return render(request, 'exam_halls/details.html', context)

def exam_hall_create(request: HttpRequest) -> HttpResponse:
    form = ExamHallCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('exam_halls:list')

    context = {
        'form': form,
        'page_title': 'Create ExamHall'
    }

    return render(request, 'exam_halls/create.html', context)

def exam_hall_edit(request: HttpRequest, pk: int) -> HttpResponse:
    searched_exam_hall = get_object_or_404(ExamHall, pk=pk)
    form = ExamHallEditForm(request.POST or None, instance=searched_exam_hall)

    if request.method == 'POST' and form.is_valid():
        if searched_exam_hall.hosted_exams.exists():
            original_hall = ExamHall.objects.get(pk=pk)
            form.instance.capacity = original_hall.capacity
            form.instance.is_computer_room = original_hall.is_computer_room

        form.save()
        return redirect('exam_halls:list')

    context = {
        'form': form,
        'page_title': f'Edit {searched_exam_hall.name}'
    }

    return render(request, 'exam_halls/edit.html', context)


def exam_hall_delete_error(request: HttpRequest) -> HttpResponse:
    context = {
        'page_title': 'Delete Error'
    }
    return render(request, 'exam_halls/delete_error.html', context)


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
