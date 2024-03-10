from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import LoginForm,RegisterForm,UserEditForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User

from rest_framework import viewsets
from .serializers import UserSerializer


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, your account is created')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'users/register.html',{'form':form})
    

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome {username}, you are logged in')
                # return redirect('homepage')
                if user.is_teacher:
                    return redirect('dashboard_teacher')
                else:
                    return redirect('homepage')

            else:
                messages.error(request,'Invalid username or password')
    else:
        login_form = LoginForm()
    return render(request,'users/login.html',{'login_form':login_form})

@login_required
def view_profile(request):
    user_profile = request.user
    return render(request, 'users/view_profile.html',{'user_profile':user_profile})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/profile_edit.html', {'form':form})

@login_required
def confirm_delete_profile(request):
    return render(request, 'users/confirm_delete_profile.html')

@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('profile_deleted')
    return redirect('view_profile')

def profile_deleted(request):
    return render(request, 'users/profile_deleted.html')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer