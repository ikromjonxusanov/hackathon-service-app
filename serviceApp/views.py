from django.shortcuts import render, redirect
from .decorators import login_required, unauthenticated
from django.contrib.auth import authenticate, login, logout
from .models import *

@login_required
def home(request):
    return render(request, 'home.html')

@unauthenticated
def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        context['error'] = "Username or/and password incorrect"
    return render(request, 'user/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def services(request):
    queryset = ServiceModel.objects.all()
    return render(request, 'services/services.html',
                  {'queryset':queryset})