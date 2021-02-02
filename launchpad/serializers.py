from rest_framework import serializers
from registry.models import Activity, Authorization, Operator, Contact, Aircraft, Pilot, Address, Person, Test, TypeCertificate, Manufacturer, TestValidity



class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

