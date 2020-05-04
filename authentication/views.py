from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect('store:book-list')
    else:
        form=AuthenticationForm()
    return render(request,'authentication/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('store:index')

def signup_view(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            # log in the user in
            return redirect("store:book-list")
    else:
        form=UserCreationForm()        
    return render(request,'authentication/signup.html',{'form':form})
