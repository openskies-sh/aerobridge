from rest_framework import serializers
from .models import Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission, CloudFile, SignedFlightLog
from registry.models import Firmware
import geojson
import arrow

class FirmwareSerializer(serializers.ModelSerializer):
    ''' A serializer for saving Firmware ''' 
    class Meta: 
        model = Firmware
        fields = '__all__'
        ordering = ['-created_at']
        
class FlightPlanListSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    class Meta:
        model = FlightPlan	
        fields = '__all__'
        ordering = ['-created_at']
    

class FlightPlanSerializer(serializers.ModelSerializer):

    def clean(self):
        cleaned_data = super().clean()

    def validate(self, data):
        """
        Check flight plan is  valid GeoJSON        """
        
        s_date = data.get("start_datetime")
        e_date = data.get("end_datetime")
        start_date = arrow.get(s_date)
        end_date = arrow.get(e_date)

        if end_date < start_date:
            raise serializers.ValidationError("End date should be greater than start date.")

        try:
            gj = geojson.loads(data['geo_json'])
        except Exception as ve:
            raise serializers.ValidationError("Not a valid GeoJSON, please enter a valid GeoJSON object")            
        
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
        
        
        
class TransactionSerializer(serializers.ModelSerializer):
    ''' A serializer to the transaction view '''

    class Meta:
        model = Transaction		
        fields = '__all__'
        ordering = ['-created_at']
        
class FlightLogSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Logs '''
    def validate(self, data):
        """
        Check flight log already exists for the operation  """

        operation_id = data.get("operation")

        if FlightLog.objects.filter(operation = operation_id).exists():
            raise serializers.ValidationError("A raw flight log has already been submitted for this operation.")        


        
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