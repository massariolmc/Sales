from django import forms
from django.forms import ModelForm, TextInput, DateInput, Select, RadioSelect, SelectDateWidget, HiddenInput, PasswordInput, EmailInput
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCustomCreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "password1", "password2")
         