from rest_framework import serializers
from .models import DigitalSkyLog, AircraftRegister
from registry.serializers import AircraftSerializer, AircraftSigningSerializer

class DigitalSkyLogSerializer(serializers.ModelSerializer):
    ''' A serializer to the drone create view '''

    class Meta:
        model = DigitalSkyLog		
        ordering = ['-created_at']
        exclude = ('created_at',)

class AircraftRegisterSerializer(serializers.ModelSerializer):

    drone = AircraftSigningSerializer(read_only=True)
    def get_drone(self, obj):
        return obj.get_drone()
    class Meta:
        model = AircraftRegister
        ordering = ['-created_at']
        fields = '__all__' 
