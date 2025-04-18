from payapp.models import UserProfile
from register.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages


User = get_user_model()
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()

            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)

            login(request, user)

            return redirect('dashboard')

    else:
        form = CustomUserCreationForm()
    return render(request, 'register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'register/dashboard.html', {'user_profile': user_profile})