from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins

from pki_framework.utils import requires_scopes
from .models import DigitalSkyLog
# Create your views here.
from .serializers import DigitalSkyLogSerializer


# @method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
# class LogList(mixins.ListModelMixin,
#               generics.GenericAPIView):
#     queryset = DigitalSkyLog.objects.all()
#     serializer_class = DigitalSkyLogSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#
# @method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
# class LogDetail(mixins.RetrieveModelMixin,
#                 generics.GenericAPIView):
#     queryset = DigitalSkyLog.objects.all()
#     serializer_class = DigitalSkyLogSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
