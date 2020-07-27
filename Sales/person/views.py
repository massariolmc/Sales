from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .forms import CompanyForm
from .models import Company, Department
from django.db import IntegrityError
from crispy_forms.utils import render_crispy_form
from django.template.loader import render_to_string
from .compress_image import delete_old_image
from django.conf import settings
import os
import json
####### COMPANY  ################

def save_form(request,form,template_name, data, user_created=None):
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
    
    return save_form(request, form, template_name, data)

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
    return save_form(request, form, template_name, data, user_created=user_created)
    
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
    
########### FIM COMPANY############################