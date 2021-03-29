from rest_framework import serializers
from pki_framework.models import DigitalSkyCredentials
from . import encrpytion_util
from djano.conf import settings

class DigitalSkyCredentialsSerializer(serializers.ModelSerializer):
    digital_sky_token = SerializerMethodField()

    def get_digital_sky_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        f = encrpytion_util.EncrpytionHelper(secret_key= settings.ENCRYPTION_KEY)
        digital_sky_token = f.decrypt(token)
        return digital_sky_token

    class Meta:
        model = DigitalSkyCredentials
        fields = ('digital_sky_token', 'name', 'token_type', 'id',)
