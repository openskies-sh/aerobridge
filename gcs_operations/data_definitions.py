from dataclasses import dataclass
import uuid
from typing import List


@dataclass
class PermissionObject:
    '''A class to hold information about Flight Permission '''
    flight_plan_id: uuid
    flight_operation_id: uuid
    flight_plan_kml_hash: str



@dataclass
class Circle:
    center: List
    radius: float


@dataclass
class GeoFenceCircle:
    version: int
    circle: Circle
    inclusion: bool

    
@dataclass
class GeoFencePolygon:
    inclusion: bool
    polygon:  List
    version: str

@dataclass
class PlanFileGeoFence:
    circles: List[GeoFenceCircle]
    polygon: List[GeoFencePolygon]
    version:int 

@dataclass
class PlanFileMission:
    pass

@dataclass
class PlanFileRallyPoints:
    pass


@dataclass
class PlanFile:
    fileType: str
    geoFence: PlanFileGeoFence
    groundStation: str
    mission: PlanFileMission        
    version: int
    rallyPoints: PlanFileRallyPoints