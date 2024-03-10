from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

############### Class for login page ###############

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super(LoginForm, self).__init__(*args, **kwargs)

            if self.request:
                self.fields['next'] = forms.CharField(widget=forms.HiddenInput, initial='/teacher/home/')

############### Class for the registration page ###############

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required = False,
        widget = forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required = False,
        widget = forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    USER_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = forms.ChoiceField(
        label='User Type',
        choices=USER_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','avatar','password1','password2','user_type']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.is_student = self.cleaned_data['user_type'] == 'student'
        user.is_teacher = self.cleaned_data['user_type'] == 'teacher'
        if commit:
            user.save()
        return user


############### Form for editing the user ###############

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','avatar')