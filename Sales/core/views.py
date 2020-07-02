from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# USER
from Sales.account.forms import UserCustomCreateForm
from Sales.account.models import User

# Create your views here.
def home(request):
    template_name = 'core/home.html'
    return render(request,template_name,{})


def signup(request):
    if request.method == 'POST':
        form = UserCustomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup:url_signup_list')
    else:
        form = UserCustomCreateForm()
       
    return render(request, 'core/signup_form.html',{'form': form})

def signup_list(request):
    template_name = 'core/signup_list.html'
    obj = User.objects.all()
    data = {
        'objects': obj
    }
    return render(request,template_name,data)

def signup_edit(request,pk):
    template_name = 'core/signup_form.html'    
    obj = get_object_or_404(User, pk=pk)
    form = UserCustomCreateForm(request.POST or None, instance=obj)
    if request.method == 'POST':        
        if form.is_valid():
            form.save()
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
    return redirect('signup:url_signup_list')


