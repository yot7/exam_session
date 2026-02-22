from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from majors.forms import MajorCreateForm, MajorEditForm, MajorDeleteForm, MajorSearchFrom
from majors.models import Major


# Create your views here.
def majors_list(request: HttpRequest) -> HttpResponse:
    search_form = MajorSearchFrom(request.GET or None)

    list_majors = Major.objects.annotate(
        total_exams=Count('exams')
    )

    if 'query' in request.GET:
        if search_form.is_valid():
            list_majors = list_majors.filter(
                Q(name__icontains=search_form.cleaned_data['query'])
            )

    context = {
        'list_majors': list_majors,
        'page_title': 'Majors',
        'search_form': search_form
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

def major_create(request: HttpRequest) -> HttpResponse:
    form = MajorCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('majors:list')

    context = {
        'form': form,
        'page_title': 'Create Major'
    }

    return render(request, 'majors/create.html', context)

def major_edit(request: HttpRequest, pk: int) -> HttpResponse:
    searched_major = get_object_or_404(Major, pk=pk)
    form = MajorEditForm(request.POST or None, instance=searched_major)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('majors:list')

    context = {
        'form': form,
        'page_title': f'Edit {searched_major.name}'
    }

    return render(request, 'majors/edit.html', context)

def major_delete(request: HttpRequest, pk: int) -> HttpResponse:
    searched_major = get_object_or_404(Major, pk=pk)
    form = MajorDeleteForm(request.POST or None, instance=searched_major)

    if request.method == 'POST' and form.is_valid():
        searched_major.delete()
        return redirect('majors:list')

    context = {
        'form': form,
        'page_title': f'Delete {searched_major.name}'
    }

    return render(request, 'majors/delete.html', context)
