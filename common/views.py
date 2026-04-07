import asyncio
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from accounts.models import ExamSessionUser
from exam_halls.models import ExamHall
from exams.models import Exam
from majors.models import Major
from faculties.models import Faculty


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    list_faculties = Faculty.objects.all()
    user_faculties = None

    if request.user.is_authenticated and request.user.majors.exists():
        user_faculties = Faculty.objects.filter(majors__users=request.user).distinct()
        list_faculties = list_faculties.exclude(id__in=user_faculties.values_list('id', flat=True))

    context = {
        'list_faculties': list_faculties,
        'user_faculties': user_faculties,
        'page_title': 'Home'
    }

    return render(request, 'common/home.html', context)


async def async_dashboard_stats(request: HttpRequest) -> HttpResponse:
    users_count, halls_count, majors_count, exams_count = await asyncio.gather(
        ExamSessionUser.objects.acount(),
        ExamHall.objects.acount(),
        Major.objects.acount(),
        Exam.objects.acount()
    )

    context = {
        'page_title': 'About Us',
        'users_count': users_count,
        'halls_count': halls_count,
        'majors_count': majors_count,
        'exams_count': exams_count,
    }

    return render(request, 'common/dashboard.html', context)