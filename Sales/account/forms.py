from django import forms
from django.forms import ModelForm, TextInput, DateInput, Select, RadioSelect, SelectDateWidget, HiddenInput, PasswordInput, EmailInput
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML, Hidden
from .models import User


class UserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "password1", "password2")
    
    def clean_cpf(self): # No caso aqui clean_nome_do_campo        
        cpf = self.cleaned_data['cpf']
        if not cpf.isdigit():                              
            raise ValidationError("Aceita apenas números.")
        return cpf # sempre retornar um dado, de preferencia o valor que estava no campo.
    def __init__(self, *args, **kwargs):                                    
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()        
        self.helper.layout = Layout(                                                                   
            Row(
                Column('cpf', css_class='form-group col-md-4 mb-0'),
                Column('first_name', css_class='form-group col-md-4 mb-0'),                
                Column('last_name', css_class='form-group col-md-4 mb-0'),                
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),                                
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),                                
                css_class='form-row'
            ),
            HTML('''
                <hr class="divider" />
                 <div class="row">    
                    <div class="col-sm-6">
                        <span class="float-left">
                            <button type="submit" class="btn btn-primary">{{ save }}</button>  	  
                            <button type="reset" class="btn btn-secondary">{{ clear }}</button>
                        </span>
                    </div>
                    <div class="col-sm-6">
                        <span class="float-right">
                            <a href="{% url 'person:url_people_list'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),
        )

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "is_active")

        