from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import CompanyForm
from .models import Company, Department
from django.db import IntegrityError
from crispy_forms.utils import render_crispy_form
from django.template.loader import render_to_string
from .compress_image import delete_old_image

####### COMPANY  ################

def save_form(request,form,template_name, data, user_created=None):
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:                               
                obj.user_created = user_created                              
            obj.save()
            return redirect('person:url_companies_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def company_create(request):
    template_name = 'company/form.html'    
    data = {"title": "Cadastro de Empresas"}    
    if request.method == 'POST':                       
        form = CompanyForm(request.POST, request.FILES)                
    else:
        form = CompanyForm()             
    
    return save_form(request, form, template_name, data)

def company_edit(request, pk):    
    template_name='company/form.html'
    data = {"title": "Editar"}    
    company = get_object_or_404(Company, pk=pk)           
    user_created = company.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = CompanyForm(request.POST, request.FILES, instance=company)                
    else:
        form = CompanyForm(instance=company)       
    return save_form(request, form, template_name, data, user_created)
    
def companies_list(request):
    template_name = "company/list.html"
    companies = Company.objects.all()    
    context = {
        'companies': companies,
        'title': "Empresas Cadastradas"       
    }
    return render(request,template_name,context)

def company_detail(request, pk=None):
    template_name = "company/detail.html"
    company = get_object_or_404(Company,pk=pk)
    context = {
        'company': company
    }
    return render(request, template_name, context)



def company_delete(request,pk):    
    company = get_object_or_404(Company, pk=pk)    
    if request.method == 'POST':        
       try:
           company.delete()
           messages.success(request, 'Ação concluída com sucesso.')
           return redirect('person:url_companies_list')
       except IntegrityError:
           messages.warning(request, 'Não é possível excluir. Esta Empresa possui departamento existentes.')
           return redirect('person:url_companies_list')    

def company_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [int(x) for x in context]      
        if context:                
            b = Company.objects.filter(id__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, 'Ação concluída com sucesso.')
    else:
        messages.warning(request, 'Não é possível excluir. Esta Empresa possui departamento existentes.')
    
    return redirect('person:url_companies_list')
    
########### FIM COMPANY############################