from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def common_auth_view(request,form_class, form_instance, template_name, success_redirect):
    if request.method == 'POST':
        if isinstance(form_instance, RegistrationForm):
            form =form_instance
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(success_redirect)
        elif isinstance(form_instance, AuthenticationForm):
            form = form_instance
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(success_redirect)
    else:
        form = form_class()
    return render(request, template_name, {'form': form})

def user_login(request):
    form=AuthenticationForm(request,data=request.POST)
    return common_auth_view(request,AuthenticationForm, form, 'userauth/login.html', 'profile')

def register(request):
    form=RegistrationForm(request.POST)
    return common_auth_view(request,RegistrationForm, form, 'userauth/register.html', 'profile')

@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'userauth/profile.html', {'user': user})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')
