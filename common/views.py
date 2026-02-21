from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from exam_halls.models import ExamHall
from exams.models import Exam
from majors.models import Major


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    last_added_major = Major.objects.order_by('-created_at').first()
    last_added_exam = Exam.objects.order_by('-created_at').first()
    total_exams = Exam.objects.all().count()
    total_exam_halls = ExamHall.objects.all().count()

    context = {
        'last_added_major': last_added_major,
        'last_added_exam': last_added_exam,
        'total_exams': total_exams,
        'total_exam_halls': total_exam_halls,
        'page_title': 'Home'
    }

    return render(request, 'common/home.html', context)
