from django import forms

from common.mixins import DisableFormFieldsMixin
from faculties.models import Faculty


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'description', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter faculty name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter faculty location'}),
        }

class FacultyDeleteForm(DisableFormFieldsMixin, FacultyForm):
    ...