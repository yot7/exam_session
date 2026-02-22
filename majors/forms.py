from django import forms

from common.mixins import DisableFormFieldsMixin
from majors.models import Major


class MajorFormBasic(forms.ModelForm):
    class Meta:
        exclude = ['slug']
        model = Major
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e. g. Computer Science'}),
            'description': forms.Textarea,
        }

class MajorCreateForm(MajorFormBasic):
    ...

class MajorEditForm(MajorFormBasic):
    ...

class MajorDeleteForm(DisableFormFieldsMixin, MajorFormBasic):
    ...

class MajorSearchFrom(forms.Form):
    query = forms.CharField(
        max_length=50,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}),
    )
