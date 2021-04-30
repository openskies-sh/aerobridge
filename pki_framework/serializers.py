from rest_framework import serializers
from pki_framework.models import DigitalSkyCredentials
from . import encrpytion_util
from django.conf import settings

class DigitalSkyCredentialsSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    token_type = serializers.SerializerMethodField()
    
    def get_token_type(self, obj):
        return obj.get_token_type_display()
    
    def get_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        f = encrpytion_util.EncrpytionHelper(secret_key= settings.ENCRYPTION_KEY)
        digital_sky_token = f.decrypt(token)
        return digital_sky_token

    class Meta:
        model = DigitalSkyCredentials
        fields = ('token', 'name', 'token_type', 'environment', 'id',)

class DigitalSkyCredentialsGetSerializer(serializers.ModelSerializer):
    token_type = serializers.SerializerMethodField()
    def get_token_type(self, obj):
        return obj.get_token_type_display()
    class Meta:
        model = DigitalSkyCredentials
        fields = ('name', 'token_type', 'environment', 'id',)
