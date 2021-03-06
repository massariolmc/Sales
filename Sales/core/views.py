from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string

# USER
from Sales.account.forms import UserCreationForm, UserChangeForm
from Sales.account.models import User
from django.db.models import Q



# Create your views here.
def home(request):    
    template_name = 'core/home.html'   
    return render(request,template_name,{})


def signup_create(request):
    context = {
        "title": _("Create User"),
        "back":_("Back"),
        "save":_("Save"),
        "clear":_("Clear"),
    } 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup:url_signup_list')
    else:
        form = UserCreationForm()
    context['form'] = form 
    return render(request, 'core/signup_form.html',{'form': form})

def signup_list(request):
    template_name = 'core/signup_list.html'
    obj = User.objects.all()
    data = dict()    

    def pagination(request,obj,lines=10):
        page = request.GET.get('page', 1)
        print("Valor de page: ",page)
        paginator = Paginator(obj, int(lines))        
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        return users

    if request.is_ajax():
        query = request.GET.get('q')
        lines = request.GET.get('l')        
        if query:
            obj = User.objects.filter(
                Q(cpf__icontains=query) | Q(first_name__icontains=query) |
                Q(last_name__icontains=query) | Q(email__icontains=query) | Q(created_at__icontains=query)
            ).distinct() 
        else:
            print("Não existe") 

        users = pagination(request,obj,int(lines))                           
    
        data['html_signup_list'] = render_to_string('core/_signup_table_list.html', {'objects': users})       
        return JsonResponse(data)
            
                 
    lines = 10
    users = pagination(request,obj,int(lines))   
    data = {
        'objects': users
    }    
    return render(request,template_name,data)

def signup_edit(request,pk):
    template_name = 'core/signup_edit.html'    
    obj = get_object_or_404(User, pk=pk)
    form = UserChangeForm(request.POST or None, instance=obj)
    if request.method == 'POST':        
        if form.is_valid():
            form.save()
            messages.success(request, 'Ação concluída com sucesso.')
            return redirect('signup:url_signup_list')       
    data = { 'form': form}
    return render(request, template_name,data)

def signup_detail(request,pk):
    template_name = 'core/signup_detail.html'
    obj = User.objects.get(pk=pk)
    data = {
        'object': obj
    }
    return render(request, template_name,data)

def signup_delete(request,pk):
    #obj = get_object_or_404(User, pk=pk)
    #obj.delete()
    messages.success(request, 'Ação concluída com sucesso.')
    messages.error(request, 'Ação concluída com sucesso.')    
    return redirect('signup:url_signup_list')

def signup_delete_all(request):
    data = {}
    context = []
    context = request.GET.get("del","")
    print("valor do context", context)
    messages.success(request, 'entrei no delete all.')            
    context = context.replace("[","").replace("]","").replace('\"','')
    context = context.split(",")
    context = [int(x) for x in context]      
    if context:                
        b = User.objects.filter(id__in=context).update(is_active=False)
        print("Valor do b",b)

    return JsonResponse(data)
        
        
    


