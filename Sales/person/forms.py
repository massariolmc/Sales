from django.forms import ModelForm, TextInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput
from .models import Company, Department
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML, Hidden
from django.core.exceptions import ValidationError

class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'fantasy_name': TextInput(attrs={'class': 'form-control'}),
            'cnpj': TextInput(attrs={'class': 'form-control'}),
            'number_state': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'slug': TextInput(attrs={'class': 'form-control'}),
            'image': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'address_number': TextInput(attrs={'class': 'form-control'}),
            'neighborhood': TextInput(attrs={'class': 'form-control'}),            
            'city': TextInput(attrs={'class': 'form-control'}),
            'state': TextInput(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            'phone_1': TextInput(attrs={'class': 'form-control'}),                        
            'phone_2': TextInput(attrs={'class': 'form-control'}),                                    
        }        
        
    #VALIDAÇÃO
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        tam = len(cnpj)        
        if tam > 0 and tam < 14:
            raise ValidationError("O CNPJ deve ter 14 digitos.")
        return cnpj

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout( 
            Hidden('user_created', '{{ user.id }}'),
            Hidden('user_updated', '{{ user.id }}'),                                   
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('fantasy_name', css_class='form-group col-md-3 mb-0'),
                Column('cnpj', css_class='form-group col-md-3 mb-0'),
                Column('number_state', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),        
            Row(
                Column('address', css_class='form-group col-md-4 mb-0'),
                Column('address_number', css_class='form-group col-md-4 mb-0'),
                Column('neighborhood', css_class='form-group col-md-4 mb-0'),                              
                css_class='form-row'
            ),           
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),                                                
                css_class='form-row'
            ),
             Row(
                Column('phone_1', css_class='form-group col-md-4 mb-0'),
                Column('phone_2', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),                                                
                css_class='form-row'
            ),
            Row(                
                Column('image', css_class='form-group col-md-3 mb-0'),
                Column('description', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),
            HTML('''
                 <div class="row">    
                    <div class="col-sm-6">
                        <span class="float-left">
                            <button type="submit" class="btn btn-primary">Salvar</button>  	  
                            <button type="reset" class="btn btn-secondary">Limpar formulário</button>
                        </span>
                    </div>
                    <div class="col-sm-6">
                        <span class="float-right">
                            <a href="{% url 'person:url_companies_list'%}" class="btn btn-warning">Voltar</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )