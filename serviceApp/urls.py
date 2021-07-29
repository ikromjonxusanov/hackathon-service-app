from django.urls import path
from .views import BotUserGenericMixins, OrderGenericMixins, ServiceGenericMixins
urlpatterns = [
    path('service/', ServiceGenericMixins.as_view()),
    path('service/<int:id>', ServiceGenericMixins.as_view()),
    path('order/', OrderGenericMixins.as_view()),
    path('order/<int:id>', OrderGenericMixins.as_view()),
    path('user/', BotUserGenericMixins.as_view()),
    path('user/<int:id>', BotUserGenericMixins.as_view()),
] 