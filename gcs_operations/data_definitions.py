from dataclasses import dataclass
import uuid
from typing import List, NamedTuple, Union


class LatLng(NamedTuple):
    latitude:float
    longitude: float

@dataclass
class PermissionObject:
    '''A class to hold information about Flight Permission '''
    flight_plan_id: uuid
    flight_operation_id: uuid
    flight_plan_kml_hash: str

@dataclass
class Circle:
    center: LatLng
    radius: float


@dataclass
class GeoFenceCircle:
    version: int
    circle: Circle
    inclusion: bool

@dataclass
class SimpleMissionItem:
    AMSLAltAboveTerrain: str
    Altitude: int
    AltitudeMode: int
    AutoContinue:bool
    Command:int
    DoJumpId: int
    Frame: int
    Params : List
    Type : str = "SimpleItem"

@dataclass
class CameraCalcData:
    AdjustedFootprintFrontal: int
    AdjustedFootprintSide: int
    CameraName: str
    DistanceToSurface: int
    DistanceToSurfaceRelative: bool
    version: int

@dataclass
class TransectStyleComplexItem:
    CameraCalc: CameraCalcData
    CameraTriggerInTurnAround: bool
    CameraShots: int
    FollowTerrain: bool
    HoverAndCapture: bool 
    Items: List[SimpleMissionItem]
    Refly90Degrees: bool
    TurnAroundDistance: bool 
    VisualTransectPoints: List

@dataclass 
class ComplexMissionItem:
    TransectStyleComplexItem: TransectStyleComplexItem
    Angle: int
    ComplexItemType: str
    EntryLocation: int
    FlyAlternateTransects: bool
    Polygon: List[LatLng]
    Polyline: List[LatLng]
    Type: str
    Version: int
    EntryPoint: int
    CorridorWidth: int

# @dataclass
# class GeoFencePolygon:
#     inclusion: bool
#     polygon:  List[LatLng]
#     version: str

# @dataclass
# class PlanFileGeoFence:
#     circles: List[GeoFenceCircle]
#     polygon: List[GeoFencePolygon]
#     version:int 

@dataclass
class PlanFileMission: 
    CruiseSpeed: int
    FirmwareType: int
    HoverSpeed: int
    Items: List[Union[SimpleMissionItem,ComplexMissionItem]]
    PlannedHomePosition: List
    VehicleType: int
    Version: int

@dataclass
class PlanFile:
    ''' For more information about the schema please refer: https://dev.qgroundcontrol.com/master/en/file_formats/plan.html, at this stage we will not be processing GeoFence and Rally points part of the flight plan.'''
    FileType: str    
    Mission: PlanFileMission
    Version: int
    GroundStation: str = 'QGroundControl'
    