from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet
from .models import Company, Department, Position, Person
from Sales.account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML, Hidden
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['name','abbreviation', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'abbreviation': TextInput(attrs={'class': 'form-control'}),                    
            'description': Textarea(attrs={'class': 'form-control'}),                    
        }            
        
    # #VALIDAÇÃO    
    def clean_name(self):        
        name = self.cleaned_data['name']           
        msg = _("There is a name for this Company. Choose other name. ")
        n = False
        if self.instance.id:
            n = Department.objects.filter(name__iexact=name, company__slug=self.instance.company.slug).exclude(id=self.instance.id).exists()#Verifica se o nome já existe                                  
        
        if n:
            raise ValidationError(msg)

        return name

class BaseDepartmentFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.company =  kwargs.get('company',None)        
        del(kwargs['company'])
        super().__init__(*args, **kwargs)        
        self.queryset = Department.objects.none() 
    
    def clean(self):
        super().clean()

        for form in self.forms:
            name = form.cleaned_data['name']
            msg = _("There is a name for this Company. Choose other name. ")
            n=False
            if form.instance.id:
                n = Department.objects.filter(name__iexact=name, company__slug=self.company).exclude(id=form.instance.id).exists()#Verifica se o nome já existe        
                
            else:            
                n = Department.objects.filter(name__iexact=name, company__slug=self.company).exists()#Verifica se o nome já existe        
                
            if n:            
                form.add_error('name', msg)  


            #form.cleaned_data['name'] = name
            # update the instance value.
            #form.instance.name = name

class PositionForm(ModelForm):
    
    class Meta:
        model = Position
        fields = ['name','description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),                                
            'description': TextInput(attrs={'class': 'form-control'}),            
        }     

class BasePositionFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.department =  kwargs.get('department',None)        
        del(kwargs['department'])
        super().__init__(*args, **kwargs)        
        self.queryset = Position.objects.filter(department__id=self.department)            
        
class PersonForm(ModelForm):

    class Meta:
        model = Person
        fields = ['name','birthday','gender','fathers_name','mothers_name','blood_type','rg','rg_exped','rg_uf','birthplace','birthplace_state','maritalstatus','pis_pasep','work_portifolio_number','work_portifolio_serie','work_portifolio_state','voter_title_number','voter_title_zone','voter_title_section','voter_title_state','drivers_license_number','drivers_license_state','drivers_license_validate','drivers_license_category','address','address_number','address_neighborhood','address_city','address_state','zip_code','phone_1','phone_2','image', 'user']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'birthday': DateInput(attrs={'class': 'form-control', 'data-inputmask-alias':'datetime', 'data-inputmask-inputformat':'dd/mm/yyyy'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'fathers_name': TextInput(attrs={'class': 'form-control'}),
            'mothers_name': TextInput(attrs={'class': 'form-control'}),            
            'blood_type': Select(attrs={'class': 'form-control'}),
            'rg': TextInput(attrs={'class': 'form-control'}),
            'rg_exped': TextInput(attrs={'class': 'form-control'}),
            'rg_uf': Select(attrs={'class': 'form-control'}),
            'birthplace': TextInput(attrs={'class': 'form-control'}),
            'birthplace_state': Select(attrs={'class': 'form-control'}),
            'maritalstatus': Select(attrs={'class': 'form-control'}),            
            'pis_pasep': TextInput(attrs={'class': 'form-control'}),
            'work_portifolio_number': TextInput(attrs={'class': 'form-control'}),
            'work_portifolio_serie': TextInput(attrs={'class': 'form-control'}),
            'work_portifolio_state': Select(attrs={'class': 'form-control'}),
            'voter_title_number': TextInput(attrs={'class': 'form-control'}),
            'voter_title_zone': TextInput(attrs={'class': 'form-control'}),
            'voter_title_section': TextInput(attrs={'class': 'form-control'}),            
            'voter_title_state': Select(attrs={'class': 'form-control'}),
            'drivers_license_number': TextInput(attrs={'class': 'form-control'}),
            'drivers_license_state': Select(attrs={'class': 'form-control'}),
            'drivers_license_validate': DateInput(attrs={'class': 'form-control', 'data-inputmask-alias':'datetime', 'data-inputmask-inputformat':'dd/mm/yyyy'}),
            'drivers_license_category': Select(attrs={'class': 'form-control'}),          
            'address': TextInput(attrs={'class': 'form-control'}),
            'address_number': TextInput(attrs={'class': 'form-control'}),
            'address_neighborhood': TextInput(attrs={'class': 'form-control'}),            
            'address_city': TextInput(attrs={'class': 'form-control'}),
            'address_state': Select(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            'phone_1': TextInput(attrs={'class': 'form-control'}),                        
            'phone_2': TextInput(attrs={'class': 'form-control'}),
            'image': FileInput(attrs={'class': 'form-control'}),                        
            'user': Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),                                    
        }           
        
    #VALIDAÇÃO    
    def clean_image(self):        
        image = self.cleaned_data['image']
        msg =  _("Maximum size allowed")
        if image:      
            if image.size > 3000000:
                raise ValidationError(msg)
        return image
    
    def __init__(self, *args, **kwargs):                                    
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label= None       
        self.fields['user'].queryset = User.objects.filter(username=self.instance.user.username)
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(                                                       
            Row(
                Column('image', css_class='form-group col-md-12 mb-0'),             
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('user', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),
            Row(               
                Column('birthday', css_class='form-group col-md-3 mb-0'),                              
                Column('gender', css_class='form-group col-md-3 mb-0'),
                Column('birthplace', css_class='form-group col-md-3 mb-0'),
                Column('birthplace_state', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fathers_name', css_class='form-group col-md-6 mb-0'),
                Column('mothers_name', css_class='form-group col-md-6 mb-0'),                               
                css_class='form-row'
            ),
            Row(
                Column('rg', css_class='form-group col-md-3 mb-0'),
                Column('rg_exped', css_class='form-group col-md-3 mb-0'),
                Column('rg_uf', css_class='form-group col-md-3 mb-0'),
                Column('maritalstatus', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),  
            Row(
                Column('pis_pasep', css_class='form-group col-md-3 mb-0'),
                Column('work_portifolio_number', css_class='form-group col-md-3 mb-0'),
                Column('work_portifolio_serie', css_class='form-group col-md-3 mb-0'),
                Column('work_portifolio_state', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),  
            Row(
                Column('voter_title_number', css_class='form-group col-md-3 mb-0'),
                Column('voter_title_zone', css_class='form-group col-md-3 mb-0'),
                Column('voter_title_section', css_class='form-group col-md-3 mb-0'),
                Column('voter_title_state', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),   
            Row(
                Column('drivers_license_number', css_class='form-group col-md-3 mb-0'),
                Column('drivers_license_state', css_class='form-group col-md-3 mb-0'),
                Column('drivers_license_validate', css_class='form-group col-md-3 mb-0'),
                Column('drivers_license_category', css_class='form-group col-md-3 mb-0'),                
                css_class='form-row'
            ),    
            Row(
                Column('address', css_class='form-group col-md-4 mb-0'),
                Column('address_number', css_class='form-group col-md-4 mb-0'),
                Column('address_neighborhood', css_class='form-group col-md-4 mb-0'),                              
                css_class='form-row'
            ),           
            Row(
                Column('address_city', css_class='form-group col-md-4 mb-0'),
                Column('address_state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),                                                
                css_class='form-row'
            ),
             Row(
                Column('phone_1', css_class='form-group col-md-4 mb-0'),
                Column('phone_2', css_class='form-group col-md-4 mb-0'),                
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
