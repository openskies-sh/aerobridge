import datetime
import json

from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils import translation
from django.views.generic import TemplateView
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DigitalSkyCredentials
from .serializers import (DigitalSkyCredentialsSerializer)
from django.http import JsonResponse
from rest_framework.decorators import api_view



from django.conf import settings
from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
from . import encrpytion_util

# Create your views here.


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class DigitalSkyCredentialsList(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                   generics.GenericAPIView):
    """
    List all operators, or create a new operator.
    """

    queryset = DigitalSkyCredentials.objects.all()
    serializer_class = DigitalSkyCredentialsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class DigitalSkyCredentialsDetail(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                               generics.GenericAPIView):
    """
    Retrieve, update or delete a Operator instance.
    """

    queryset = DigitalSkyCredentials.objects.all()
    serializer_class = DigitalSkyCredentialsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



