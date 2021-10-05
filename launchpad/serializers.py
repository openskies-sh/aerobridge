from rest_framework import serializers
from registry.models import Activity, Operator, Contact, Aircraft, Pilot, Address, Person, Manufacturer, Firmware, Contact, Pilot, Engine, Authorization
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class PersonSerializer(serializers.ModelSerializer):
         
    # def validate(self, data):
    #     """
    #     Check flight plan is  valid alphanumeric
    #     """
        
    #     id_isalnum = data['identification_document'].isalnum()
    #     try:
    #         assert id_isalnum
    #     except AssertionError as ae:        
    #         raise serializers.ValidationError("ID must be alpha numeric")            
    #     else:
    #         return data
    class Meta:
        model = Person
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OperatorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Operator
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        exclude=('is_registered',)


class ManufacturerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'

class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class AuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        fields = '__all__'
