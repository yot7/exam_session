from django import forms

from common.mixins import DisableFormFieldsMixin
from majors.models import Major


class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        exclude = ['slug']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e. g. Computer Science'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description'}),
        }

class MajorDeleteForm(DisableFormFieldsMixin, MajorForm):
    ...

class MajorSearchFrom(forms.Form):
    query = forms.CharField(
        max_length=50,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}),
    )
