from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from majors.models import Major

UserModel = get_user_model()

class MajorModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj: Major):
        return obj.name

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        help_text='Required. Inform a valid email address.',
    )
    username = forms.CharField(
        max_length=50,
    )
    first_name = forms.CharField(
        max_length=50, 
        required=False,
    )
    last_name = forms.CharField(
        max_length=50,
    )
    academic_rank = forms.CharField(
        disabled=True,
        required=False,
        help_text='Contact administration to set your academic rank.',
        initial='Student',
    )
    majors = MajorModelMultipleChoiceField(
        queryset=Major.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text='Please select your major/s.',
    )

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'first_name', 'last_name', 'academic_rank', 'majors']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'majors':
                field.widget.attrs['class'] = 'form-control'
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data['majors']:
                user.majors.set(self.cleaned_data['majors'])
            
            student_group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            
        return user
