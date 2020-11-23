from rest_framework import serializers
from .models import Drone



class DroneSerializer(serializers.ModelSerializer):
    ''' A serializer to the drone create view '''

    class Meta:
        model = Drone		
        ordering = ['-created_at']
        exclude = ('operator_business_id',)
