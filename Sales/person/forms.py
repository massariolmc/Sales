from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from .models import Company, Department, PersonType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML, Hidden
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ['name','fantasy_name','cnpj','number_state','email','image','description','address','address_number','neighborhood','city','state','zip_code','phone_1','phone_2']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'fantasy_name': TextInput(attrs={'class': 'form-control'}),
            'cnpj': TextInput(attrs={'class': 'form-control'}),
            'number_state': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),            
            'image': FileInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'address_number': TextInput(attrs={'class': 'form-control'}),
            'neighborhood': TextInput(attrs={'class': 'form-control'}),            
            'city': TextInput(attrs={'class': 'form-control'}),
            'state': TextInput(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            'phone_1': TextInput(attrs={'class': 'form-control'}),                        
            'phone_2': TextInput(attrs={'class': 'form-control'}),                                    
        }
        # error_message = {
        #     'cnpj': _("This field CNPJ exactly needs 14 digits. "),
        #     'image': _("Maximum size allowed")
        # }        
        
    #VALIDAÇÃO
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        msg =  _("This field CNPJ exactly needs 14 digits. ")
        tam = len(cnpj)        
        if tam > 0 and tam < 14:
            raise ValidationError(msg)
        return cnpj
    
    def clean_image(self):        
        image = self.cleaned_data['image']
        msg =  _("Maximum size allowed")
        if image:      
            if image.size > 3000000:
                raise ValidationError(msg)
        return image
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(                                               
            Row(
                Column('image', css_class='form-group col-md-12 mb-0'),             
                css_class='form-row'
            ),
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
                Column('description', css_class='form-group col-md-12 mb-0'),                
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
                            <a href="{% url 'person:url_companies_list'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )


class DepartmentForm(ModelForm):

    class Meta:
        model = Department
        fields = ['name','abbreviation','company','description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'abbreviation': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'company': Select(attrs={'class': 'form-control'}),                                                                     
        }             
        
    #VALIDAÇÃO    
    def clean(self):        
        name = self.cleaned_data['name']           
        company_id = self.cleaned_data['company']                
        msg = _("There is a name for this Company. Choose other name. ")
        if self.instance.id:
            n = Department.objects.filter(name__iexact=name, company_id=self.instance.company_id).exclude(id=self.instance.id).exists()#Verifica se o nome já existe        
            
        else:            
            n = Department.objects.filter(name__iexact=name, company_id=company_id).exists()#Verifica se o nome já existe        
            
        if n:            
            self.add_error('name', msg)

class PersonTypeForm(ModelForm):

    class Meta:
        model = PersonType
        fields = ['name','max_discount','company','description','block_discount']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'max_discount': NumberInput(attrs={'class': 'form-control'}),            
            'company': Select(attrs={'class': 'form-control'}),        
            'description': Textarea(attrs={'class': 'form-control'}),
            #'block_discount': CheckboxInput(attrs={'class': 'form-control'}),                                                             
        }             
        
    #VALIDAÇÃO    
    def clean(self):        
        name = self.cleaned_data['name']           
        company_id = self.cleaned_data['company']                
        msg = _("There is a person type for this Company. Choose other name. ")
        if self.instance.id:
            n = PersonType.objects.filter(name__iexact=name, company_id=self.instance.company_id).exclude(id=self.instance.id).exists()#Verifica se o nome já existe        
            
        else:            
            n = PersonType.objects.filter(name__iexact=name, company_id=company_id).exists()#Verifica se o nome já existe        
            
        if n:            
            self.add_error('name', msg)