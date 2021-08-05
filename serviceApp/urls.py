from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('services/', services, name="services"),

]