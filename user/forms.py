from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from public.models import Lottery


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Repeat Password'}))


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}))


class NewLotteryForm(ModelForm):
    finish = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'id': 'id_finish',
            'type': 'text'
        })
    )

    class Meta:
        model = Lottery
        fields = ['name', 'description', 'thumbnail', 'count_ticket', 'ticket_price', 'finish']
