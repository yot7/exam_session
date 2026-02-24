from django import forms

from common.mixins import DisableFormFieldsMixin
from exam_halls.models import ExamHall


class ExamHallFormBasic(forms.ModelForm):
    class Meta:
        model = ExamHall
        fields = '__all__'
        widgets = {
            'capacity': forms.NumberInput(attrs={
                'initial': 50,
                'min': 15,
                'max': 400,
                'step': 5,
            }),
        }
        labels = {
            'name': 'Room name:',
            'is_computer_room': 'Is this a computer room?'
        }

    def clean(self):
        cleaned_data = super().clean()

        if not 15 <= cleaned_data.get('capacity') <= 400:
            self.add_error('capacity', 'Capacity must be between 15 and 400')

        return cleaned_data

class ExamHallCreateForm(ExamHallFormBasic):
    ...

class ExamHallEditForm(ExamHallFormBasic):
    ...

class ExamHallDeleteForm(DisableFormFieldsMixin, ExamHallFormBasic):
    ...

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
