
from rest_framework import generics, mixins

from .models import AerobridgeCredential
from .serializers import (AerobridgeCredentialGetSerializer, AerobridgeCredentialPostSerializer)
from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class CredentialsList(APIView):
    """
    List all tokens, or create a new token.
    """


    def get(self, request, format=None):
        credentials = AerobridgeCredential.objects.all()
        serializer = AerobridgeCredentialGetSerializer(credentials, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        serializer = AerobridgeCredentialPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class CredentialsDetail(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    Update or delete a token instance.
    """

    queryset = AerobridgeCredential.objects.all()
    serializer_class = AerobridgeCredentialGetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

