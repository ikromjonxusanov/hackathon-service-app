from django.forms import *
from .models import CategoryModel, ServiceModel, OrderModel

class CategoryServiceForm(ModelForm):
    class Meta:
        model = ServiceModel
        fields = "__all__"
        exclude = ['category']

class CategoryForm(ModelForm):
    class Meta:
        model = CategoryModel
        fields = "__all__"

class ServiceForm(ModelForm):
    class Meta:
        model = ServiceModel
        fields = "__all__"

class OrderForm(ModelForm):
    class Meta:
        model = OrderModel
        fields = "__all__"

