from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from majors.models import Major


# Create your views here.
def majors_list(request: HttpRequest) -> HttpResponse:
    list_majors = Major.objects.annotate(
        total_exams=Count('exams')
    )

    context = {
        'list_majors': list_majors,
        'page_title': 'Majors'
    }

    return render(request, 'majors/list.html', context)

def major_details(request: HttpRequest, slug: str) -> HttpResponse:
    searched_major = get_object_or_404(
        Major.objects.prefetch_related('exams'),
        slug=slug,
    )

    context = {
        'searched_major': searched_major,
        'page_title': f'{searched_major.name} Details'
    }

    return render(request, 'majors/details.html', context)
