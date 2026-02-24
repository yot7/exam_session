from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum, Min

from common.mixins import DisableFormFieldsMixin
from exam_halls.models import ExamHall
from exams.validators import validate_start_time, validate_end_time
from majors.models import Major
from exams.models import Exam


class ExamSearchForm(forms.Form):
    query = forms.CharField(
        max_length=50,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}),
    )
    date = forms.DateField(
        required=False,
        label='Exam date:',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '1900-01-01',
            'max': '3000-12-31',
        }),
    )

class PrepExamFormBasic(forms.Form):
    subject = forms.CharField(
        max_length=50,
        label='Exam subject:',
    )
    major = forms.ModelChoiceField(
        queryset=Major.objects.all(),
        label='Related Major:',
    )
    needs_computers = forms.BooleanField(initial=False, required=False)
    number_of_examinees = forms.IntegerField(
        min_value=15,
        max_value=400,
        initial=15,
        label='Number of examinees:',
        widget=forms.NumberInput(attrs={'min': 15, 'max': 400, 'step': 5}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '1900-01-01',
            'max': '3000-12-31',
        }),
        label='Exam date:',
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'min': '08:00',
            'max': '19:00',
            'step': timedelta(hours=1),
        }),
        label='Exam start time:',
        validators=[validate_start_time],
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'min': '09:00',
            'max': '20:00',
            'step': timedelta(hours=1),
        }),
        label='Exam end time:',
        validators=[validate_end_time],
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        subject = cleaned_data.get('subject')
        major = cleaned_data.get('major')

        if start and end:
            if end <= start:
                self.add_error('end_time', 'Exam must be at least an hour long')

        if subject and major:
            if Exam.objects.filter(subject=subject, major=major).exists():
                raise ValidationError(f"An exam for '{subject}' in '{major}' already exists.")

        return cleaned_data

class ExamHallModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj: ExamHall):
        return f"{obj.name} (Capacity: {obj.capacity})"

class ExamFormBasic(forms.Form):
    exam_halls = ExamHallModelMultipleChoiceField(
        queryset=ExamHall.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Available exam halls:',
        required=False,
    )
    needed_capacity = forms.IntegerField(
        disabled=True,
        label='Needed capacity:',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        step0_data = kwargs.pop('step0_data', None)
        super().__init__(*args, **kwargs)

        if step0_data:
            selected_date = step0_data['date']
            selected_start_time = step0_data['start_time']
            selected_end_time = step0_data['end_time']
            unavailable_halls = ExamHall.objects.prefetch_related('hosted_exams').filter(hosted_exams__date=selected_date)
            unavailable_halls_ids = []

            for hall in unavailable_halls:
                for exam in hall.hosted_exams.filter(date=selected_date):
                    if max(exam.start_time, selected_start_time) < min(exam.end_time, selected_end_time):
                        unavailable_halls_ids.append(hall.id)
                        break

            available_halls = ExamHall.objects.exclude(id__in=unavailable_halls_ids).filter(
                is_computer_room=step0_data['needs_computers']
            )

            self.fields['exam_halls'].queryset = available_halls
            self.fields['needed_capacity'].initial = step0_data['number_of_examinees']
            self.needed_capacity = step0_data['number_of_examinees']
            self.exam_halls = available_halls

    def clean(self):
        cleaned_data = super().clean()
        if ((self.exam_halls.exists() and
                self.exam_halls.aggregate(Sum('capacity'))['capacity__sum'] < self.needed_capacity)
                or self.exam_halls.count() == 0):
            self.fields['exam_halls'].disabled = True
            raise ValidationError(
                "Not enough space for the exam on the chosen date and hours."
                "If there are no other available halls, please go back and select a different date or hours."
            )
        else:
            selected_halls = cleaned_data.get('exam_halls')
            total_selected_capacity = selected_halls.aggregate(Sum('capacity'))['capacity__sum'] if selected_halls else 0

            if total_selected_capacity < self.needed_capacity:
                self.add_error('exam_halls', 'Not enough space for the exam in the selected halls. Please select more.')
            elif total_selected_capacity - selected_halls.aggregate(Min('capacity'))['capacity__min'] >= self.needed_capacity:
                raise ValidationError('Selected halls have too much space. Please select fewer exam halls.')

        return cleaned_data

class PrepExamFormCreate(PrepExamFormBasic):
    ...

class ExamFormCreate(ExamFormBasic):
    ...

class PrepExamFormEdit(PrepExamFormBasic):
    def clean(self):
        cleaned_data = super(PrepExamFormBasic, self).clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        subject = cleaned_data.get('subject')
        major = cleaned_data.get('major')

        if start and end:
            if end <= start:
                self.add_error('end_time', 'Exam must be at least an hour long')

        if subject and major:
            exam_pk = self.initial.get('exam_pk')
            
            unique_key_violations = Exam.objects.filter(subject=subject, major=major)
            if exam_pk:
                unique_key_violations = unique_key_violations.exclude(pk=exam_pk)
            
            if unique_key_violations.exists():
                raise ValidationError(f"An exam for '{subject}' in '{major}' already exists.")

        return cleaned_data

class ExamFormEdit(ExamFormBasic):
    def __init__(self, *args, **kwargs):
        step0_data = kwargs.get('step0_data', None)
        
        super().__init__(*args, **kwargs)

        if step0_data:
            selected_date = step0_data['date']
            selected_start_time = step0_data['start_time']
            selected_end_time = step0_data['end_time']
            unavailable_halls = ExamHall.objects.prefetch_related('hosted_exams').filter(hosted_exams__date=selected_date)
            unavailable_halls_ids = set()
            current_rooms = set()
            
            exam_pk = self.initial.get('exam_pk')

            for hall in unavailable_halls:
                for exam in hall.hosted_exams.filter(date=selected_date):

                    if exam_pk and exam.pk == exam_pk:
                        current_rooms.add(hall.id)
                        continue

                    if max(exam.start_time, selected_start_time) < min(exam.end_time, selected_end_time):
                        unavailable_halls_ids.add(hall.id)
                        break

            available_halls = ExamHall.objects.exclude(
                id__in=unavailable_halls_ids.difference(current_rooms)
            ).filter(
                is_computer_room=step0_data['needs_computers']
            )

            self.fields['exam_halls'].queryset = available_halls
            self.fields['needed_capacity'].initial = step0_data['number_of_examinees']
            self.needed_capacity = step0_data['number_of_examinees']
            self.exam_halls = available_halls

class ExamDeleteForm(DisableFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exam_halls'].queryset = self.instance.exam_halls.all()