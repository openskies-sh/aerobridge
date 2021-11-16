from django.db.models.query_utils import select_related_descend
from rest_framework import serializers
from .models import Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission, CloudFile, SignedFlightLog
from registry.models import Firmware
import json
import arrow
from .data_definitions import PlanFile, PlanFileMission, SimpleMissionItem, ComplexMissionItem, TransectStyleComplexItem, CameraCalcData



class FirmwareSerializer(serializers.ModelSerializer):
    ''' A serializer for saving Firmware ''' 
    class Meta: 
        model = Firmware
        fields = '__all__'
        ordering = ['-created_at']
        
class FlightPlanSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''

    def process_simple_item(self, mission_item):         
        ''' A class to generate a simple mission ite,'''       
        try:
            amsl_alt = mission_item['AMSLAltAboveTerrain']
        except KeyError as ke:
            amsl_alt = 0
        try:
            alt = mission_item['Altitude']
        except KeyError as ke:
            alt = 0
        try:
            alt_mode = mission_item['AltitudeMode']
        except KeyError as ke:
            alt_mode = 0
        try:
            auto_continue = mission_item['autoContinue']
        except KeyError as ke:
            auto_continue = 0
            
        try:
            command = mission_item['command']
        except KeyError as ke:
            command = 0
        try:
            jump_id = mission_item['doJumpId']
        except KeyError as ke:
            jump_id = 0
        try:
            params = mission_item['params']
        except KeyError as ke:
            params = 0
        try:
            frame = mission_item['frame']
        except KeyError as ke:
            frame = 0



        simple_mission = SimpleMissionItem(AMSLAltAboveTerrain=amsl_alt, Altitude=alt, AltitudeMode=alt_mode, AutoContinue= auto_continue, Command=command,DoJumpId= jump_id,Params = params, Frame= frame)

        return simple_mission

    def validate(self, data):
        """
        Check flight plan is valid KML        
        """
        # TODO: Validate a Flight Plan JSON, definition here: https://dev.qgroundcontrol.com/master/en/file_formats/plan.html#TransectStyleComplexItem
        plan_file_json = data['plan_file_json']
        mission = plan_file_json['mission']
        
        mission_items = mission['items']
        all_mission_items = []
        for mission_item in mission_items:
            mission_type = mission_item['type']
            if (mission_type == "SimpleItem"):

                simple_mission = self.process_simple_item(mission_item)
                all_mission_items.append(simple_mission)

            elif (mission_type == "ComplexItem"):
                
                try:
                    amsl_alt = mission_item['AMSLAltAboveTerrain']
                except KeyError as ke:
                    amsl_alt = 0
                try:
                    angle = mission_item['angle']
                except KeyError as ke:
                    angle = 0
                try:
                    complex_item_type = mission_item['complexItemType']
                except KeyError as ke:
                    complex_item_type = 0
                try:
                    entry_location = mission_item['entryLocation']
                except KeyError as ke:
                    entry_location = 0
                try:
                    refly_90_degrees = mission_item['Refly90Degrees']
                except KeyError as ke:
                    refly_90_degrees = 0
                try:
                    turn_around_disatnce = mission_item['TurnAroundDistance']
                except KeyError as ke:
                    turn_around_disatnce = 0
            
            
                try:
                    virtual_transect_points = mission_item['VisualTransectPoints']
                except KeyError as ke:
                    virtual_transect_points = 0

                entry_point = mission_item['EntryPoint']

                corridor_width = mission_item['CorridorWidth']

                transect_style_complex_item = mission_item['TransectStyleComplexItem']

                camera_calc = transect_style_complex_item['CameraCalc']
                camera_shots = transect_style_complex_item['CameraShots']
                camera_trigger_in_turn_around = transect_style_complex_item['CameraTriggerInTurnAround']
                follow_terrain = transect_style_complex_item['FollowTerrain']
                hover_and_capture = transect_style_complex_item['HoverAndCapture']

                camera_calc_data = CameraCalcData(AdjustedFootprintFrontal= camera_calc['AdjustedFootprintFrontal'],AdjustedFootprintSide = camera_calc['AdjustedFootprintSide'],CameraName = camera_calc['CameraName'],  DistanceToSurface=camera_calc['DistanceToSurface'] ,DistanceToSurfaceRelative = camera_calc['DistanceToSurfaceRelative'], version=camera_calc['version'] )
                
                all_items = transect_style_complex_item['Items']
                all_simple_items = []
                for item in all_items:
                    if item['type'] == 'SimpleItem':
                        simple_mission = self.process_simple_item(item)

                        all_simple_items.append(simple_mission)


                transect_style_complex_item =TransectStyleComplexItem(CameraCalc = camera_calc_data,CameraShots =camera_shots , CameraTriggerInTurnAround =camera_trigger_in_turn_around , FollowTerrain =follow_terrain, HoverAndCapture= hover_and_capture, Items = all_simple_items,Refly90Degrees = refly_90_degrees, TurnAroundDistance = turn_around_disatnce, VisualTransectPoints =virtual_transect_points)
             
                try:
                    fly_alternate_transects = mission_item['flyAlternateTransects']
                except KeyError as ke:
                    fly_alternate_transects = 0
                try:
                    c_mission_type = mission_item['type']
                except KeyError as ke:
                    c_mission_type = 0
                try:
                    polygon = mission_item['polygon']
                except KeyError as ke:
                    polygon = 0
                try:
                    version = mission_item['version']
                except KeyError as ke:
                    version = 0

                complex_mission = ComplexMissionItem(EntryPoint= entry_point, CorridorWidth = corridor_width, TransectStyleComplexItem= transect_style_complex_item, Angle=angle, ComplexItemType=complex_item_type, EntryLocation= entry_location, FlyAlternateTransects=fly_alternate_transects,Type= c_mission_type,Version = version, Polygon= polygon)
                all_mission_items.append(complex_mission)


            else:
                raise serializers.ValidationError("Only a ComplexItem or SimpleItem mission type are supported")
       

        m = PlanFileMission(CruiseSpeed=mission['cruiseSpeed'],FirmwareType = mission['firmwareType'],HoverSpeed= mission['hoverSpeed'] , PlannedHomePosition = mission['plannedHomePosition'], VehicleType = mission['vehicleType'], Version = mission['version'], Items = all_mission_items)
        
        pf = PlanFile(FileType = plan_file_json['fileType'],Version = plan_file_json['version'], GroundStation = plan_file_json['groundStation'], Mission = m)

        return data

    def create(self, validated_data):

        # TODO: Convert a FlightPlan JSON to a GeoJSON

        return super(FlightPlanSerializer, self).create(validated_data)
    class Meta:
        model = FlightPlan	
        exclude = ('is_editable','geo_json',)
        ordering = ['-created_at']

class FlightOperationListSerializer(serializers.ModelSerializer):
    ''' A serializer for Flight Operations '''
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