from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    USER_CHOICES = (
        ('leader', 'Leader'),
        ('player', 'Player'),
    )
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    type_user = forms.ChoiceField(choices=USER_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'type_user', 'password1', 'password2', )