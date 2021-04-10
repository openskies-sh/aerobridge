
from rest_framework import generics, mixins

from .models import DigitalSkyCredentials
from .serializers import (DigitalSkyCredentialsSerializer,DigitalSkyCredentialsGetSerializer)
from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
from . import encrpytion_util
from .forms import TokenCreateForm
# Create your views here.

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class DigitalSkyCredentialsList(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                   generics.GenericAPIView):
    """
    List all tokens, or create a new token.
    """

    queryset = DigitalSkyCredentials.objects.all()
    serializer_class = DigitalSkyCredentialsSerializer
    form_class = TokenCreateForm

    def form_valid(self, form):
        token = form.instance.token
        form.instance.token = encrpytion_util.encrypt(token)
        return super(DigitalSkyCredentialsList, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
        
@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class DigitalSkyCredentialsDetail(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    Update or delete a token instance.
    """

    queryset = DigitalSkyCredentials.objects.all()
    serializer_class = DigitalSkyCredentialsGetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

