from django.db.models.query_utils import select_related_descend
from rest_framework import serializers
from .models import Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission, CloudFile, SignedFlightLog
from registry.models import Firmware
import json
import arrow
from fastkml import kml

class FirmwareSerializer(serializers.ModelSerializer):
    ''' A serializer for saving Firmware ''' 
    class Meta: 
        model = Firmware
        fields = '__all__'
        ordering = ['-created_at']
        
class   FlightPlanListSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    class Meta:
        model = FlightPlan	
        fields = '__all__'
        ordering = ['-created_at']
    

class FlightPlanSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Check flight plan is  valid KML        
        """
        
        s_date = data.get("start_datetime")
        e_date = data.get("end_datetime")
        start_date = arrow.get(s_date)
        end_date = arrow.get(e_date)

        if end_date < start_date:
            raise serializers.ValidationError("End date should be greater than start date.")

        try:
            k = kml.KML()            
            k.from_string(data['kml'])
            data['kml'] = k.to_string()

        except Exception as ve:
            raise serializers.ValidationError("Not a valid KML, please enter a valid KML object")            
        
        return data

    class Meta:
        model = FlightPlan		
        exclude = ('is_editable',)
        ordering = ['-created_at']

class FlightOperationListSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    class Meta:
        model = FlightOperation	
        fields = '__all__'
        ordering = ['-created_at']

     
 
class FlightOperationSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    # drone = AircraftDetailSerializer(read_only=True)
    # flight_plan = FlightPlanSerializer(read_only=True)
    class Meta:
        model = FlightOperation	
        exclude = ('is_editable',)
        ordering = ['-created_at']
        
class FlightPermissionSerializer(serializers.ModelSerializer):
    operation = FlightOperationSerializer(read_only=True)
    class Meta:
        model = FlightPermission	
        fields = '__all__'	
        ordering = ['-created_at']
        
        
class FlightOperationPermissionSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    permission = serializers.SerializerMethodField()
    
    def get_permission(self, obj):
        permission = FlightPermission.objects.get(operation_id = obj.id)
        return permission.json
    class Meta:
        model = FlightOperation	
        fields = ('operation_id', 'permission')
        ordering = ['-created_at']
    
        
# class TransactionSerializer(serializers.ModelSerializer):
#     ''' A serializer to the transaction view '''

#     class Meta:
#         model = Transaction		
#         fields = '__all__'
#         ordering = ['-created_at']
        
class FlightLogSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Logs '''
    def validate(self, data):
        """
        Check flight log already exists for the operation  """

        raw_log = data.get("raw_log")
        try: 
            json.loads(raw_log)
        except TypeError as te:
            raise serializers.ValidationError("A raw flight log must be a valid JSON object")        
        return data

        
    class Meta:
        model = FlightLog	
        exclude = ('is_submitted','is_editable',)
        ordering = ['-created_at']
 
class SignedFlightLogSerializer(serializers.ModelSerializer):
    ''' A serializer for Signed Flight Logs '''
    class Meta:
        model = SignedFlightLog	        
        ordering = ['-created_at']
        fields = '__all__'


class CloudFileSerializer(serializers.ModelSerializer):
    ''' A serializer for Cloud Files '''
    class Meta:
        model = CloudFile
        fields = '__all__'
        ordering = ['-created_at']