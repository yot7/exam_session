from django import forms
from django.core.exceptions import ValidationError

from common.mixins import DisableFormFieldsMixin
from exam_halls.models import ExamHall


class ExamHallFormBasic(forms.ModelForm):
    class Meta:
        model = ExamHall
        fields = ['name', 'capacity', 'is_computer_room', 'faculty']
        widgets = {
            'capacity': forms.NumberInput(attrs={
                'initial': 50,
                'min': 15,
                'max': 400,
                'step': 5,
            }),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Room name:',
            'is_computer_room': 'Is this a computer room?'
        }

    def clean(self):
        cleaned_data = super().clean()

        if not 15 <= cleaned_data.get('capacity') <= 400:
            self.add_error('capacity', 'Capacity must be between 15 and 400')

        faculty = cleaned_data.get('faculty')
        name = cleaned_data.get('name')

        if name and faculty:
            if ExamHall.objects.filter(name=name, faculty=faculty).exists():
                raise ValidationError(f'An exam hall with the name "{name}" already exists in this faculty.')

        return cleaned_data

class ExamHallCreateForm(ExamHallFormBasic):
    ...

class ExamHallEditForm(ExamHallFormBasic):
    def clean(self):
        cleaned_data = super().clean()

        faculty = cleaned_data.get('faculty')
        name = cleaned_data.get('name')

        if name and faculty:
            exam_hall_pk = self.initial.get('exam_hall_pk')

            unique_key_violations = ExamHall.objects.filter(name=name, faculty=faculty)
            if exam_hall_pk:
                unique_key_violations = unique_key_violations.exclude(pk=exam_hall_pk)

            if unique_key_violations.exists():
                raise ValidationError(f'An exam hall with the name "{name}" already exists in this faculty.')

        return cleaned_data

class ExamHallDeleteForm(DisableFormFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExamHall
        fields = ['name', 'capacity', 'is_computer_room', 'faculty']
        labels = {
            'name': 'Room name:',
            'is_computer_room': 'Is this a computer room?'
        }


class ExamHallSearchFrom(forms.Form):
    query = forms.CharField(
        max_length=50,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}),
    )
    is_computer_room = forms.BooleanField(
        required=False,
        label='Show computer rooms only',
    )
    min_capacity = forms.IntegerField(
        min_value=15,
        max_value=400,
        required=False,
        initial=15,
        label='Minimum capacity:',
    )
