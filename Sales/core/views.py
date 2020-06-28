from django.shortcuts import render, redirect
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
            return redirect('home')
    else:
        form = UserCustomCreateForm()
       
    return render(request, 'core/signup.html',{'form': form})