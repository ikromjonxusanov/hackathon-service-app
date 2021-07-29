from re import U
from serviceApp.serializer import BotUserSerializer
from rest_framework import serializers
import rest_framework
from rest_framework.views import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from .serializer import BotUserSerializer, ServiceSerializer, OrderSerializer
from .models import BotUserModel, ServiceModel, OrderModel

class BotUserGenericMixins(GenericAPIView,
                            ListModelMixin,
                            RetrieveModelMixin,
                            CreateModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin):
    serializer_class = BotUserSerializer
    queryset = BotUserModel.objects.all()
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        return Response({'error':"Not found id"})
    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        return Response({'error':"Not found id"})

class ServiceGenericMixins(GenericAPIView,
                            ListModelMixin,
                            RetrieveModelMixin,
                            CreateModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin):
    serializer_class = ServiceSerializer
    queryset = ServiceModel.objects.all()
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        return Response({'error':"Not found id"})
    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        return Response({'error':"Not found id"})

class OrderGenericMixins(GenericAPIView,
                            ListModelMixin,
                            RetrieveModelMixin,
                            CreateModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        if id:
            return self.update(request, pk)
        return Response({'error':"Not found id"})
    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        return Response({'error':"Not found id"})
    