from rest_framework import serializers
from pki_framework.models import DigitalSkyCredentials
from . import encrpytion_util
from djano.conf import settings

class DigitalSkyCredentialsSerializer(serializers.ModelSerializer):
    token = SerializerMethodField()

    def get_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        f = encrpytion_util.EncrpytionHelper(secret_key= settings.ENCRYPTION_KEY)
        digital_sky_token = f.decrypt(token)
        return digital_sky_token

    class Meta:
        model = DigitalSkyCredentials
        fields = ('token', 'name', 'token_type', 'id',)

class DigitalSkyCredentialsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DigitalSkyCredentials
        fields = ('name', 'token_type', 'id',)
