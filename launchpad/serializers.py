from rest_framework import serializers
from registry.models import Activity, AircraftComponentSignature, AircraftMasterComponent, AircraftModel, Operator, Contact, Aircraft, AircraftDetail, Pilot, Address, Person, Manufacturer, Firmware, Contact, Pilot, Authorization, AircraftComponent, AircraftAssembly
from gcs_operations.models import FlightPlan


class PersonSerializer(serializers.ModelSerializer):         
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
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class AuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        fields = '__all__'

class AircraftDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftDetail
        fields = '__all__'

class FlightPlanReadSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
    class Meta:
        model = FlightPlan	
        exclude = '__all__'
        ordering = ['-created_at']


class AircraftComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftComponent
        exclude = ('is_active',)

class AircraftComponentSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftComponentSignature
        fields = '__all__'

class AircraftModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = '__all__'

class AircraftAssemblySerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name')
    status_type = serializers.SerializerMethodField()
    def get_status_type(self, obj):
        x = obj.get_status_display()        
        return x
  
    class Meta:
        model = AircraftAssembly
        fields = ('id','model_name','status_type','model','updated_at',)

class AircraftMasterComponentSerializer(serializers.ModelSerializer):
    # def get_installed_model(self, obj):
    #     x = 
    linked_models = serializers.SerializerMethodField()
    family = serializers.SerializerMethodField()
    def get_family(self, obj):        
        x = obj.get_family_display()   
        return x

    def get_linked_models(self, obj):        
        x = obj.aircraftmodel_set.all()
        name_series = []
        for x1 in x: 
            name_series.append(x1.name + ' / Series ' + x1.series)
        return ','.join(name_series)
    class Meta:
        model = AircraftMasterComponent
        fields = ('name','family','drawing', 'linked_models', 'created_at', 'updated_at',)
