from django.shortcuts import render, redirect, get_object_or_404
from .decorators import login_required, unauthenticated
from django.contrib.auth import authenticate, login, logout
from .models import BotUserModel, CategoryModel, OrderModel, ServiceModel
from .forms import CategoryForm, ServiceForm, OrderForm, CategoryServiceForm

def get_object_or_Home(Class, pk):
    try:
        return Class.objects.get(id=pk)
    except:
        return redirect('/')

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
        if user is not None:
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
    categories = CategoryModel.objects.all()
    try:
        activeCategory = int(request.GET.get('category'))
    except:
        activeCategory = None
    if activeCategory:
        queryset = ServiceModel.objects.filter(category_id=activeCategory)
    else:
        queryset = ServiceModel.objects.all()
    return render(request, 'services/services.html',
                  {'queryset':queryset, 'categories':categories,
                   'active':activeCategory,
                   })
def category_service_create(request, pk):
    object = get_object_or_Home(CategoryModel, pk)
    form = CategoryServiceForm()
    if request.method == "POST":
        form = CategoryServiceForm()
        if form.is_valid():
            cs_form = form.save(commit=False)
            cs_form.category = object
            cs_form.save()
            return redirect('/')
    return render(request, 'c-s/create.html', {"form":form, 'name':f'{object} create service'})
def categoryCreate(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    return render(request, 'c-s/create.html', {'form':form, "name":"Service Category"})

def categoryUpdate(request, pk):

    object = get_object_or_Home(CategoryModel, pk)
    form = CategoryForm(instance=object)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('services')
    return render(request, 'c-s/update.html', {'form':form, "name":"Service Category"})

def categoryDelete(request, pk):
    object = get_object_or_Home(CategoryModel, pk)
    if request.method == "POST":
        object.delete()
        return redirect('services')
    return render(request, 'c-s/delete.html',
                  {'object':object,"name":"Service Category"})

def serviceCreate(request):
    form = ServiceForm()
    if request.method == "POST":
        form = ServiceForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('services')
    return render(request, 'c-s/create.html', {'form':form,"name":"Service Category"})

def serviceUpdate(request, pk):

    object = get_object_or_Home(ServiceModel, pk)
    form = ServiceForm(instance=object)
    if request.method == "POST":
        form = ServiceForm(data=request.POST, files=request.FILES, instance=object)
        if form.is_valid():
            form.save()
            return redirect('services')
    return render(request, 'c-s/update.html', {'form':form, "name":"Service Category"})

def serviceDelete(request, pk):
    object = get_object_or_Home(CategoryModel, pk)
    if request.method == "POST":
        object.delete()
        return redirect('services')
    return render(request, 'c-s/delete.html',
                  {'object':object, "name":"Service Category"})