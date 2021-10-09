import requests
import os, json
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
import datetime
from rest_framework import status
from django.utils.decorators import method_decorator
from .models import DigitalSkyLog
import json
from rest_framework.response import Response
# Create your views here.



# @method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
# class LogList(mixins.ListModelMixin,
#                   generics.GenericAPIView):
#     queryset = DigitalSkyLog.objects.all()
#     serializer_class = DigitalSkyLogSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# @method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
# class LogDetail(mixins.RetrieveModelMixin,
#                     generics.GenericAPIView):
#     queryset = DigitalSkyLog.objects.all()
#     serializer_class = DigitalSkyLogSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
