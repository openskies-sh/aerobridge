from rest_framework import serializers
from .models import DigitalSkyLog



class DigitalSkyLogSerializer(serializers.ModelSerializer):
    ''' A serializer to the drone create view '''

    class Meta:
        model = DigitalSkyLog		
        ordering = ['-created_at']
        exclude = ('created_at',)
