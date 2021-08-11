from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('s/', services, name="services"),

    path('c/create/', categoryCreate, name="c-create"),
    path('c/<int:pk>/create/', category_service_create, name="cs-create"),
    path('c/update/<int:pk>', categoryUpdate, name="c-update"),
    path('c/delete/<int:pk>', categoryDelete, name="c-delete"),

    path('s/create/', serviceCreate, name="s-create"),
    path('s/update/<int:pk>', serviceUpdate, name="s-update"),
    path('s/delete/<int:pk>', serviceDelete, name="s-delete"),
]