from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from exam_halls.models import ExamHall


# Create your views here.
def exam_halls_list(request: HttpRequest) -> HttpResponse:
    list_exam_halls = ExamHall.objects.all()

    context = {
        'list_exam_halls': list_exam_halls,
        'page_title': 'Exam Halls'
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
