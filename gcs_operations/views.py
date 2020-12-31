from django.shortcuts import render
from rest_framework import mixins
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from .serializers import TransactionSerializer
from .models import Transaction
from rest_framework import status
from django.utils.decorators import method_decorator

from functools import wraps
from django.http import JsonResponse
from pki_framework.utils import requires_scopes

# Create your views here.



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class TransactionList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class TransactionDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


