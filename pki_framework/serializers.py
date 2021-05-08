from rest_framework import serializers
from pki_framework.models import AerobridgeCredential
from . import encrpytion_util
from django.conf import settings

class AerobridgeCredentialSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    token_type = serializers.SerializerMethodField()
    
    def get_token_type(self, obj):
        return obj.get_token_type_display()
    
    def get_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')
        
        f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
        t = f.decrypt(token)
        t = t.decode('utf-8')
        return t

    class Meta:
        model = AerobridgeCredential
        fields = ('token', 'name', 'token_type', 'association', 'id',)

class AerobridgeCredentialGetSerializer(serializers.ModelSerializer):
    token_type = serializers.SerializerMethodField()
    def get_token_type(self, obj):
        return obj.get_token_type_display()
    class Meta:
        model = AerobridgeCredential
        fields = ('name', 'token_type', 'association', 'id',)
