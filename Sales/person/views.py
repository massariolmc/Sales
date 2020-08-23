from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .forms import CompanyForm, DepartmentForm, PersonTypeForm
from .models import Company, Department, PersonType
from django.db import IntegrityError
from crispy_forms.utils import render_crispy_form
from django.template.loader import render_to_string
#from .compress_image import delete_old_image
#from django.conf import settings
import os
import json
####### COMPANY  ################

def company_save_form(request,form,template_name, data, user_created=None):
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            return redirect('person:url_companies_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def company_create(request):
    template_name = 'company/form.html'    
    data = {
            "title": _("Create Company"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = CompanyForm(request.POST, request.FILES)                
    else:
        form = CompanyForm()             
    
    return company_save_form(request, form, template_name, data)

def company_edit(request, slug):    
    template_name='company/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    company = get_object_or_404(Company, slug=slug)           
    user_created = company.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = CompanyForm(request.POST, request.FILES, instance=company)                
    else:
        form = CompanyForm(instance=company)       
    return company_save_form(request, form, template_name, data, user_created=user_created)
    
def companies_list(request):
    template_name = "company/list.html"
    companies = Company.objects.all()    
    context = {
        'companies': companies,
        'title': _("Registered Companies"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def company_detail(request, slug):    
    template_name = "company/detail.html"
    company = get_object_or_404(Company,slug=slug)
    context = {
        'company': company,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def company_delete(request, slug):    
    company = get_object_or_404(Company, slug=slug)    
    if request.method == 'POST':        
       try:
           company.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('person:url_companies_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This company has an existing department.'))
           return redirect('person:url_companies_list')    

def company_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Company.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This company has an existing department.'))
    
    return redirect('person:url_companies_list')

def company_translate_js(request):    
    if request.method == "GET":
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'templates/default')        
        translate = ""        
        with open(file_path+"/translate_data_tables-"+request.LANGUAGE_CODE+".json", 'r') as arquivo:
            for linha in arquivo:
                translate += linha        
        obj = json.loads(translate)        
    return JsonResponse(obj)
    
########### FIM COMPANY ############################

####### DEPARTMENT  ################

def department_save_form(request,form,template_name, data, user_created=None):
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            return redirect('person:url_departments_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def department_create(request):
    template_name = 'department/form.html'    
    data = {
            "title": _("Create Department"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = DepartmentForm(request.POST, request.FILES)                
    else:
        form = DepartmentForm()             
    
    return department_save_form(request, form, template_name, data)

def department_edit(request, slug):    
    template_name='department/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    department = get_object_or_404(Department, slug=slug)           
    user_created = department.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = DepartmentForm(request.POST, request.FILES, instance=department)                
    else:
        form = DepartmentForm(instance=department)       
    return department_save_form(request, form, template_name, data, user_created=user_created)
    
def departments_list(request):
    template_name = "department/list.html"
    departments = Department.objects.all()    
    context = {
        'departments': departments,
        'title': _("Registered Departments"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def department_detail(request, slug):    
    template_name = "department/detail.html"
    department = get_object_or_404(Department,slug=slug)
    context = {
        'department': department,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def department_delete(request, slug):    
    department = get_object_or_404(Department, slug=slug)    
    if request.method == 'POST':        
       try:
           department.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('person:url_departments_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This department has an existing department.'))
           return redirect('person:url_departments_list')    

def department_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Department.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This department has an existing department.'))
    
    return redirect('person:url_departments_list')

def department_translate_js(request):    
    if request.method == "GET":
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'templates/default')        
        translate = ""        
        with open(file_path+"/translate_data_tables-"+request.LANGUAGE_CODE+".json", 'r') as arquivo:
            for linha in arquivo:
                translate += linha        
        obj = json.loads(translate)        
    return JsonResponse(obj)
    
########### FIM DEPARTMENT############################


####### PERSON TYPE  ################


def person_type_save_form(request,form,template_name, data, user_created=None):
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            return redirect('person:url_person_types_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def person_type_create(request):
    template_name = 'person_type/form.html'    
    data = {
            "title": _("Create PersonType"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = PersonTypeForm(request.POST, request.FILES)                
    else:
        form = PersonTypeForm()             
    
    return person_type_save_form(request, form, template_name, data)

def person_type_edit(request, slug):    
    template_name='person_type/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    person_type = get_object_or_404(PersonType, slug=slug)           
    user_created = person_type.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = PersonTypeForm(request.POST, request.FILES, instance=person_type)                
    else:
        form = PersonTypeForm(instance=person_type)       
    return person_type_save_form(request, form, template_name, data, user_created=user_created)
    
def person_types_list(request):
    template_name = "person_type/list.html"
    person_types = PersonType.objects.all()    
    context = {
        'person_types': person_types,
        'title': _("Registered Companies"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def person_type_detail(request, slug):    
    template_name = "person_type/detail.html"
    person_type = get_object_or_404(PersonType,slug=slug)
    context = {
        'person_type': person_type,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def person_type_delete(request, slug):    
    person_type = get_object_or_404(PersonType, slug=slug)    
    if request.method == 'POST':        
       try:
           person_type.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('person:url_person_types_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This person_type has an existing department.'))
           return redirect('person:url_person_types_list')    

def person_type_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = PersonType.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This person_type has an existing department.'))
    
    return redirect('person:url_person_types_list')

def person_type_translate_js(request):    
    if request.method == "GET":
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'templates/default')        
        translate = ""        
        with open(file_path+"/translate_data_tables-"+request.LANGUAGE_CODE+".json", 'r') as arquivo:
            for linha in arquivo:
                translate += linha        
        obj = json.loads(translate)        
    return JsonResponse(obj)
    

########### FIM PERSON TYPE ############################
