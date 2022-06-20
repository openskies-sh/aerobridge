from rest_framework import serializers
from registry.models import Activity, AircraftMasterComponent, AircraftModel, Operator, Contact, Aircraft, AircraftDetail, Pilot, Address, Person, Company, Firmware, Contact, Pilot, Authorization, AircraftComponent, AircraftAssembly
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

class CompanySerializer(serializers.ModelSerializer):  
    class Meta:
        model = Company
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
    component_common_name = serializers.ReadOnlyField()
    status_display = serializers.SerializerMethodField()
    aircraft_details = serializers.SerializerMethodField()


    def get_aircraft_details(self, obj):
        return obj.aircraft_details
        
    def get_status_display(self, obj):
        x = obj.get_status_display()        
        return x
    class Meta:
        model = AircraftComponent
        exclude = ('is_active','aerobridge_id',)

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
    slugify_family = serializers.ReadOnlyField()
    procurement_origin = serializers.ReadOnlyField()
    net_stock = serializers.ReadOnlyField()
    order_price = serializers.ReadOnlyField()
    total_stock = serializers.ReadOnlyField()
    allocated_stock = serializers.ReadOnlyField()
    linked_models = serializers.SerializerMethodField()
    family = serializers.SerializerMethodField()
    assembly_names = serializers.SerializerMethodField()
    def get_assembly_names(self, obj):        
        assembly_names =[]
        if obj.assembly:
            all_assemblies = obj.mastercomponentassembly_set.all()
            for assembly in all_assemblies:
                assembly_names.append(assembly.name)
        return assembly_names

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
        fields = ('id','name','family','drawing', 'minimum_stock','linked_models','assembly','assembly_names', 'created_at', 'updated_at','slugify_family','default_supplier','order_price','total_stock','procurement_origin','net_stock','allocated_stock',)
