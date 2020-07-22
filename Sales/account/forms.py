from django import forms
from django.forms import ModelForm, TextInput, DateInput, Select, RadioSelect, SelectDateWidget, HiddenInput, PasswordInput, EmailInput
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserCustomCreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "password1", "password2")
    
    def clean_cpf(self): # No caso aqui clean_nome_do_campo        
        cpf = self.cleaned_data['cpf']
        if not cpf.isdigit():                              
            raise ValidationError("Aceita apenas números.")
        return cpf # sempre retornar um dado, de preferencia o valor que estava no campo.

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "is_active")

        