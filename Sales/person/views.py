from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
from django.contrib import messages
from .forms import CompanyForm, DepartmentForm, BaseDepartmentFormSet, PositionForm, BasePositionFormSet, PersonForm
from Sales.account.forms import  UserCreationForm
from django.forms import modelformset_factory
from .models import Company, Department, Position, Person
from Sales.account.models import User
from django.db import IntegrityError
from crispy_forms.utils import render_crispy_form
from django.template.loader import render_to_string
from django.db.models import Q
import os
import json
import datetime

####### COMPANY  ################

def create_department_situations_defaults(obj):    
    ''' 
    Cria um Departamento padrão e um Cargo padrão na momemnto da criação da Empresa  
    '''
    d = Department.objects.create(name= 'Padrão', abbreviation= 'Padrão', company= obj, user_created=obj.user_created , user_updated=obj.user_updated)
    d.save()
    s = Situation.objects.create(name= 'Funcionário', department= d, user_created=obj.user_created , user_updated=obj.user_updated)
    s.save()
    return 1

def company_save_form(request,form,template_name, data, user_created=None):
    marc = 0 # Marcador para saber se está criando ou editando 0 - Editar / 1 - Criar
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE
                marc = 1
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            if marc:
                create_department_situations_defaults(obj)
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
    
########### FIM COMPANY ############################

####### DEPARTMENT  ################

def department_save_form(request,form,template_name, context, user_created=None): 
    def save_obj(request, obj, user_created=None):
        if user_created:
            obj.user_created = user_created
            obj.user_updated = request.user            
            obj.save()
        else:
            for o in obj:                    
                o.company = context['company']                    
                o.user_updated = request.user                                    
                o.user_created = request.user
                o.save()

    data = dict()   
    if request.method == 'POST':                                                                
        if form.is_valid():
            obj = form.save(commit=False)                                        
            if user_created:# Se cair aqui é EDIT                             
                save_obj(request, obj, user_created)
            else:# Se cair aqui é CREATE                
                save_obj(request, obj)
            data['form_is_valid'] = True
            departments = Department.objects.filter(company__slug=context['company'].slug)
            objects = pagination(request,departments, 1, lines=10)
            data['html_list'] = render_to_string('department/_table_company_departments.html', {
                'departments': objects
            })
            data['html_paginate'] = render_to_string('department/_paginate.html', {'departments': objects})
        else:
            data['form_is_valid'] = False
            print("form", form)
            print("algo não está valido.")                  
    context['form'] = form    
    data['html_form'] = render_to_string(template_name, context, request=request)    
    return JsonResponse(data)

def department_create(request,company_pk):
    template_name = 'department/_form_create.html'
    company = Company.objects.get(slug=company_pk)        
    context = {
            "title": _("Create Department"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            "company": company,
        }    
    DepartmentFormSet = modelformset_factory(Department, form=DepartmentForm, formset=BaseDepartmentFormSet)  
    
    if request.method == 'POST':                              
        form = DepartmentFormSet(request.POST, request.FILES, company=company_pk)                     
    else:         
        form = DepartmentFormSet(company=company_pk)                   
    
    return department_save_form(request, form, template_name, context)

def department_edit(request, slug):    
    template_name='department/_form_edit.html'
    department = get_object_or_404(Department, slug=slug)    
    company = Company.objects.get(slug=department.company.slug)
    user_created = department.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa
    context = {            
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            'company': company,
        }
    if request.method == 'POST':        
        form = DepartmentForm(request.POST, request.FILES, instance=department)                
    else:
        form = DepartmentForm(instance=department)       
    return department_save_form(request, form, template_name, context, user_created=user_created)

def company_departments(request, company_pk):
    template_name = "department/template_shared.html"
    data=dict()
    query = request.GET.get('q',None)
    page = request.GET.get('page',None)
    lines = request.GET.get('lines',10)
    if query:                        
        departments = Department.objects.filter(company__slug=company_pk)
        departments = departments.filter(            
            Q(name__icontains=query) | Q(abbreviation__icontains=query)            
        ).distinct() 
    else:
        departments = Department.objects.filter(company__slug=company_pk)

    company = Company.objects.get(slug=company_pk)
    objects = pagination(request,departments, page, lines=lines)   
    context = {
        'company': company,
        'departments': objects,
        'title': _("Registered Departments"),
        'add': _("Add"),            
    }  
    if query or page:
        data['form_is_valid'] = True   
        data['html_list'] = render_to_string('department/_table_company_departments.html', context)       
        data['html_paginate'] = render_to_string('department/_paginate.html', context)       
        return JsonResponse(data)
    else:
        return render(request,template_name,context)    

def department_detail(request, slug):    
    template_name = "department/_detail.html"
    data=dict()
    department = get_object_or_404(Department,slug=slug)
    context = {
        'department': department,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }      
    data['html_form'] = render_to_string(template_name, context, request=request)    
    return JsonResponse(data)
    #return render(request, template_name, context)

def department_delete(request, slug): 
    template_name = "department/_delete.html"   
    department = get_object_or_404(Department, slug=slug) 
    company = department.company.slug
    data = dict()   
    if request.method == 'POST':        
       try:
            department.delete()
            data['form_is_valid'] = True
            departments = Department.objects.filter(company__slug=company)
            objects = pagination(request,departments, 1, lines=10)
            data['html_list'] = render_to_string('department/_table_company_departments.html', {
                'departments': objects
            })
            data['html_paginate'] = render_to_string('department/_paginate.html', {'departments': objects})           
       except IntegrityError:           
            context = {'department': department, 'messages': {'message':_('You cannot delete. This department has an existing department.'), 'level': 0 }}
            data['html_form'] = render_to_string(template_name,
            context,
            request=request,
            )        
        #    messages.warning(request, _('You cannot delete. This department has an existing department.'))
        #    return redirect('person:url_departments_list')    
    else:
        context = {'department': department}
        data['html_form'] = render_to_string(template_name,
            context,
            request=request,
        )
    return JsonResponse(data)
    
########### FIM DEPARTMENT############################

# VIEW PARA TRADUZIR O DATATABLES. USO GERAL
def translate_datables_js(request):    
    if request.method == "GET":
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'templates/default')        
        translate = ""        
        with open(file_path+"/translate_data_tables-"+request.LANGUAGE_CODE+".json", 'r') as arquivo:
            for linha in arquivo:
                translate += linha        
        obj = json.loads(translate)        
    return JsonResponse(obj)

####### POSITION  ################

def position_save_form(request,form,template_name, context, user_created=None):
    def save_obj(request, obj, user_created=None):
        for o in obj:
            if not o.id:# Se for falso, vai ser um create, senão edit
                o.user_created = request.user
            o.department = context['department']                    
            o.user_updated = request.user                                   
            o.save()
    data = dict()
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)
            for del_obj in form.deleted_objects:#VErifica se tem objetos para deletar
                del_obj.delete()                                               
            save_obj(request, obj)
            data['form_is_valid'] = True
            
        else:
            data['form_is_valid'] = False
            print("form", form)
            print("algo não está valido.")                                
    
    context['form'] = form    
    data['html_form'] = render_to_string(template_name, context, request=request)    
    return JsonResponse(data)

def position_create(request, department_pk):
    template_name = 'position/_form.html'    
    department = Department.objects.get(slug=department_pk)
    context = {
            "title": _("Create Positions"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            'department': department,
        }
    PositionFormSet = modelformset_factory(Position, form=PositionForm, formset=BasePositionFormSet, can_delete=True)      
    if request.method == 'POST':                       
        form = PositionFormSet(request.POST, department = department.id)                
    else:
        form = PositionFormSet(department = department.id)             
    
    return position_save_form(request, form, template_name, context)

########## FIM POSITION ############################

########### PERSON ############################
def person_save_form(request,form,template_name, data, user_created=None):
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            return redirect('person:url_people_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def create_user_and_person(request):
    template_name = 'core/signup_form.html'
    context = {
        "title": _("Create User"),
        "back":_("Back"),
        "save":_("Save"),
        "clear":_("Clear"),
    } 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            person = Person(name='{} {}'.format(obj.first_name,obj.last_name), user = obj, user_created = request.user, user_updated = request.user)
            person.save()
            return redirect('person:url_person_edit', person.slug)            
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, template_name, context)

def person_edit(request, slug):    
    template_name='person/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    person = get_object_or_404(Person, slug=slug)          
    user_created = person.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = PersonForm(request.POST, request.FILES, instance=person)                
    else:
        form = PersonForm(instance=person)       
    return person_save_form(request, form, template_name, data, user_created=user_created)
    
def people_list(request):
    template_name = "person/list.html"
    data=dict()
    query = request.GET.get('q',None)
    page = request.GET.get('page',None)
    lines = request.GET.get('lines',10)
    people = Person.objects.all()
    if query:                       
        people = people.filter(            
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__cpf__icontains=query) | Q(user__email__icontains=query)           
        ).distinct()    
    objects = pagination(request,people, page, lines=lines)
        
    context = {
        'people': objects,
        'title': _("Registered People"),
        'add': _("Add")      
    }
    if query or page:
        data['form_is_valid'] = True   
        data['html_list'] = render_to_string('person/_table.html', context)       
        data['html_paginate'] = render_to_string('person/_paginate.html', context)       
        return JsonResponse(data)
    else:
        return render(request,template_name,context) 

def person_detail(request, slug):    
    template_name = "person/detail.html"
    person = get_object_or_404(Person,slug=slug)
    context = {
        'person': person,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def person_deactive(request, slug):    
    person = get_object_or_404(Person, slug=slug) 
    #user = User.objects.filter(pk=person.user.id)       
    context = dict()
    b = {'true': True, 'false': False}
    if request.method == 'POST':        
        sw = request.POST['sw'] 
        print("valor sw", b[sw])       
        context['is_valid'] = True
        person.user.is_active = b[sw]
        person.user.save()
        context['is_active'] = b[sw]
    else:
        context['is_valid'] = False
        context['is_active'] = 'teste'                 
    
    return JsonResponse(context)

def person_delete(request, slug):  
    template_name = "person/_delete.html" 
    person = get_object_or_404(Person, slug=slug)
    user = User.objects.get(pk=person.user.id)
    data = dict()   
    if request.method == 'POST':        
       try:
            person.delete()
            user.delete()
            data['form_is_valid'] = True
            people = Person.objects.all()
            objects = pagination(request,people, 1, lines=10)
            data['html_list'] = render_to_string('person/_table.html', {
                'people': objects
            })
            data['html_paginate'] = render_to_string('person/_paginate.html', {'people': objects})           
       except IntegrityError:           
            context = {'person': department, 'messages': {'message':_('You cannot delete. This person has many relationships.'), 'level': 0 }}
            data['html_form'] = render_to_string(template_name,
            context,
            request=request,
            )                 
    else:
        context = {'person': person}
        data['html_form'] = render_to_string(template_name,
            context,
            request=request,
        )
    return JsonResponse(data)    

########### FIM PERSON ############################

########## PAGINAÇÃO USO GERAL ##########################
def pagination(request,obj,page, lines=10):
    page = request.GET.get('page', 1)
    print("Valor de page: ",page)
    paginator = Paginator(obj, int(lines))        
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return objects

########## FIM PAGINAÇÃO USO GERAL ##########################