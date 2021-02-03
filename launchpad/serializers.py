from rest_framework import serializers
from registry.models import Activity, Authorization, Operator, Contact, Aircraft, Pilot, Address, Person, Test, TypeCertificate, Manufacturer, TestValidity, Manufacturer, Firmware


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
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
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'
