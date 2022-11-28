from csv import excel
#from xxlimited import new
from rest_framework import serializers
from registry.models import Activity, AircraftMasterComponent, AircraftModel, Operator, Contact, Aircraft, AircraftDetail, Pilot, Address, Person, Company, Firmware, Contact, Pilot, Authorization, AircraftComponent, AircraftAssembly, SupplierPart
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


    assembly_component_status = serializers.SerializerMethodField()
    assembly_status = serializers.SerializerMethodField()
    assembly_id =  serializers.SerializerMethodField()
    def get_assembly_component_status(self, obj):
        assembly = obj.final_assembly
        x = assembly.components_ok
        return x
  
    
    def get_assembly_status(self, obj):
        assembly = obj.final_assembly
        x = assembly.status
        return x
  
    def get_assembly_id(self, obj):
        assembly_id = obj.final_assembly.id        
        return assembly_id
    class Meta:
        model = Aircraft
        fields = ('id','assembly_component_status','assembly_status','assembly_id','operator','name', 'flight_controller_id','status', 'final_assembly')

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


class AircraftSearchComponentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AircraftComponent
        fields = ('id','aerobridge_id')

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
        exclude = ('is_active',)

class AircraftComponentUpdateSerializer(serializers.ModelSerializer):
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


    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        new_status = validated_data.get('status', None)
        if new_status != 10:
            assemblies = AircraftAssembly.objects.filter(components = instance).distinct()
            for assembly in assemblies:
                assembly.status = 1
                aircraft = Aircraft.objects.get(final_assembly = assembly)
                aircraft.status = 0 
                assembly.save()
                aircraft.save()
        instance.save()
        return instance 
        
class AircraftModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = '__all__'

class AircraftUpdateSerializer(serializers.ModelSerializer):    
    def validate_status(self,value):
        if value:
            assembly = self.instance.final_assembly 
            components = assembly.components.all()
            for component in components: 
                if component.status != 10:
                    raise serializers.ValidationError("Cannot set the aircraft as active until the status for %(component_name)s is updated and set to OK"  %{'component_name': component.component_common_name})
        return value

    class Meta:
        model = Aircraft
        exclude = ('final_assembly','manufacturer')


class AircraftAssemblySerializer(serializers.ModelSerializer):
    aircraft_model_name = serializers.CharField(source='aircraft_model.name')
    status_type = serializers.SerializerMethodField()
    def get_status_type(self, obj):
        x = obj.get_status_display()        
        return x
  
    class Meta:
        model = AircraftAssembly
        fields = ('id','aircraft_model_name','status_type','aircraft_model','updated_at',)



# class AircraftAssemblyComponentsSerializer(serializers.ModelSerializer):
#     aircraft_model_name = serializers.CharField(source='aircraft_model.name')
#     components_to_add = serializers.MultipleChoiceField()

#     def get_components_to_add(self, obj):
#         not_found_components = []
#         # Components in the Assembly 
#         all_components = obj.components.all()

#         # Master Components that should be in the model 
#         aircraft_model = obj.aircraft_model        
#         all_master_components = aircraft_model.master_components.all()

#         is_found = False
#         for current_component in all_components:
#             supplier_part_exists = current_component.supplier_part

#             if supplier_part_exists is not None:
#                 if (current_component.supplier_part.manufacturer_part.master_component in all_master_components):
#                     is_found = True
#             else: 
#                 if current_component.master_component in all_master_components:
#                     is_found = True

#             if is_found == False:
#                 if supplier_part_exists:                     
#                     not_found_components.append(current_component.supplier_part.manufacturer_part.master_component)
#                 else:
#                     not_found_components.append(current_component.master_component.id)
        
#         return AircraftComponent.objects.filter(pk__in = not_found_components)

#     class Meta:
#         model = AircraftAssembly
#         fields = ('id','updated_at','aircraft_model_name','components_to_add')

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
    has_supplier_manufacturer_part = serializers.SerializerMethodField()
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

    def get_has_supplier_manufacturer_part(self, obj):        
        supplier_part_exists = SupplierPart.objects.filter(manufacturer_part__master_component = obj).exists()
        return supplier_part_exists
    class Meta:
        model = AircraftMasterComponent
        fields = ('id','name','family','drawing', 'minimum_stock','linked_models','assembly','assembly_names', 'created_at', 'updated_at','slugify_family','default_supplier','order_price','total_stock','procurement_origin','net_stock','allocated_stock','has_supplier_manufacturer_part',)
