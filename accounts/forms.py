from email.policy import default

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from majors.models import Major

UserModel = get_user_model()

class MajorModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj: Major):
        return obj.name

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50)
    academic_rank = forms.CharField(
        disabled=True,
        required=False,
        help_text='Contact administration to set your academic rank.',
        initial='Student',
    )
    majors = MajorModelMultipleChoiceField(
        queryset=Major.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Please select your major/s.',
    )

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'first_name', 'last_name', 'academic_rank', 'password1', 'password2']