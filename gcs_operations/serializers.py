from rest_framework import serializers
from .models import Transaction, FlightOperation, FlightPlan, FlightPermission
from registry.serializers import AircraftDetailSerializer
class FlightPlanSerializer(serializers.ModelSerializer):


    class Meta:
        model = FlightPlan		
        ordering = ['-created_at']
        
class FlightOperationSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    drone = AircraftDetailSerializer(read_only=True)
    manufacturer = FlightPlanSerializer(read_only=True)
    class Meta:
        model = FlightOperation		
        ordering = ['-created_at']
        
class FlightPermissionSerializer(serializers.ModelSerializer):
    operation = FlightOperationSerializer(read_only=True)
    class Meta:
        model = FlightPermission		
        ordering = ['-created_at']
        
class TransactionSerializer(serializers.ModelSerializer):
    ''' A serializer to the transaction view '''

    class Meta:
        model = Transaction		
        ordering = ['-created_at']
