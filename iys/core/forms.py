from django import forms
from django.contrib.auth.models import User
from core.models import Hospital


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')