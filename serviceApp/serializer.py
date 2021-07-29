from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import BotUserModel, ServiceModel, OrderModel

class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUserModel
        fields = "__all__"

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = ServiceModel
        fields = "__all__"

class OrderSerializer(ModelSerializer):
    user = BotUserSerializer()
    service = ServiceModel()
    class Meta:
        model = OrderModel
        fields = "__all__"

