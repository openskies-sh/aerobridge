from rest_framework import serializers
from pki_framework.models import AerobridgeCredential
from . import encrpytion_util
from django.conf import settings

from django.core.exceptions import ValidationError

class AerobridgeCredentialSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    token_type = serializers.SerializerMethodField()
    
    def validate(self, data):
        
        if (data['association'] == 0) and (data['operator'] is None):            
            raise serializers.ValidationError('Please select an Operator for the Operator Token')
            
        elif data['association'] in [1] and data['manufacturer'] is None:
            raise serializers.ValidationError('Please select an Manufacturer for the Manufacturer Token')

        elif data['association'] in [3] and data['aircraft'] is None:
            raise serializers.ValidationError('Please select an Aircraft for the Aircraft Token')

        return data
    def get_token_type(self, obj):
        return obj.get_token_type_display()
    
    def get_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        if isinstance(token, memoryview): #for Postgres / Django
            token = token.tobytes()
            
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')
        
        f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
        t = f.decrypt(token)
        t = t.decode('utf-8')
        return t

    class Meta:
        model = AerobridgeCredential
        fields = ('token', 'name', 'token_type','extension', 'association','is_active', 'id','aircraft','manufacturer','operator',)

class TokenField(serializers.Field):

    def to_representation(self, value):
        
        token = value
        if isinstance(token, memoryview): #for Postgres / Django
            token = token.tobytes()
            
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')
        
        f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
        t = f.decrypt(token)
        t = t.decode('utf-8')
        return t
    def to_internal_value(self, data):
        
        token = data.encode('utf-8')
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')        
        my_encryptor = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
        enc_token = my_encryptor.encrypt(message=token)
        
        return enc_token


class AerobridgeCredentialPostSerializer(serializers.ModelSerializer):
    token = TokenField()
    
    def validate(self, data):
        
        if (data['association'] == 0) and (data['operator'] is None):            
            raise serializers.ValidationError('Please select an Operator for the Operator Token')
            
        elif data['association'] in [1] and data['manufacturer'] is None:
            raise serializers.ValidationError('Please select an Manufacturer for the Manufacturer Token')

        elif data['association'] in [3] and data['aircraft'] is None:
            raise serializers.ValidationError('Please select an Aircraft for the Aircraft Token')

        return data
    

    def get_token(self, digital_sky_credentials):
        token = digital_sky_credentials.token
        if isinstance(token, memoryview): #for Postgres / Django
            token = token.tobytes()
            
    class Meta:
        model = AerobridgeCredential
        fields = ('token', 'name', 'token_type', 'extension','association','is_active', 'id','aircraft','manufacturer','operator',)

class AerobridgeCredentialGetSerializer(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField()
    token_type = serializers.SerializerMethodField()
    def get_token_type(self, obj):
        return obj.get_token_type_display()

    association = serializers.SerializerMethodField()
    def get_association(self, obj):
        return obj.get_association_display()

    # def get_token(self, digital_sky_credentials):
    #     token = digital_sky_credentials.token
    #     if isinstance(token, memoryview): #for Postgres / Django
    #         token = token.tobytes()
            
    #     secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')
        
    #     f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
    #     t = f.decrypt(token)
    #     t = t.decode('utf-8')
    #     return t

    class Meta:
        model = AerobridgeCredential
        fields = ('created_at', 'name', 'token_type', 'extension','association','is_active', 'id','aircraft','manufacturer','operator',)
        # extra_kwargs = {
        #     'token': {'write_only': True}
        # }
