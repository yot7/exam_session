from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from exams.models import Exam


# Create your views here.
def exams_list(request: HttpRequest) -> HttpResponse:
    list_exams = Exam.objects.all()

    context = {
        'list_exams': list_exams,
        'page_title': 'Exams'
    }

    return render(request, 'exams/list.html', context)

def exam_details(request: HttpRequest, pk: int) -> HttpResponse:
    searched_exam = get_object_or_404(
        Exam.objects.prefetch_related('exam_halls'),
        pk=pk,
    )

    context = {
        'searched_exam': searched_exam,
        'page_title': f'{searched_exam.subject} Details'
    }

    return render(request, 'exams/details.html', context)
