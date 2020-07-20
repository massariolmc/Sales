from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .forms import CompanyForm
from .models import Company, Department
from crispy_forms.utils import render_crispy_form
from django.template.loader import render_to_string

####### COMPANY
def save_form(request,form,template_name, data):
    if request.method == 'POST':                                       
        if form.is_valid():            
            form.save()                    
            return redirect('person:url_companies_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def company_create(request):
    template_name = 'company/form.html'    
    data = {}
    data['title'] = "Cadastro de Empresas"
    if request.method == 'POST':                       
        form = CompanyForm(request.POST)                
    else:
        form = CompanyForm()             
    
    return save_form(request, form, template_name, data)

def company_edit(request, pk):    
    template_name='company/form.html'
    data = {}    
    company = get_object_or_404(Company, pk=pk)        
    user_created = company.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':                       
        form = CompanyForm(request.POST, instance=company)                
    else:
        form = CompanyForm(instance=company)             
    
    return save_form(request, form, template_name, data)
    
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
    #if request.method == 'GET':        
    #    try:
    #        company.delete()
    #        messages.success(request, 'Ação concluída com sucesso.')
    #        return redirect('url_companies_list')
    #    except IntegrityError:
    #        messages.warning(request, 'Não é possível excluir. Esta Empresa possui departamento existentes.')
    #        return redirect('url_companies_list') 
    #else:
    messages.warning(request, 'Ação teste.')
    return redirect('person:url_companies_list')

def company_delete_all(request):    
    data = {}
    context = []
    context = request.GET.get("del","")
    print("valor do context", context)
    messages.success(request, 'entrei no delete all.')            
    context = context.replace("[","").replace("]","").replace('\"','')
    context = context.split(",")
    context = [int(x) for x in context]      
    #if context:                
    #     b = User.objects.filter(id__in=context).update(is_active=False)
    #     print("Valor do b",b)
    #companies = Company.objects.all()
    #data['html_list'] = render_to_string('company/list.html', {'companies': companies})       
    return JsonResponse(data)    

########### FIM COMPANY############################

