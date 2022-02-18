from dataclasses import dataclass
import uuid
import enum
import arrow
from typing import List, Literal


class StringBasedDateTime(str):
  """String that only allows values which describe a datetime."""
  def __new__(cls, value):
    if isinstance(value, str):
      t = arrow.get(value).datetime
    else:
      t = value
    str_value = str.__new__(cls, arrow.get(t).to('UTC').format('YYYY-MM-DDTHH:mm:ss.SSSSSS') + 'Z')
    str_value.datetime = t
    return str_value


@dataclass
class LatLngPoint:
    '''A clas to hold information about LatLngPoint'''
    lat: float
    lng: float

@dataclass
class Radius:
    ''' A class to hold the radius object '''
    value: float
    units:str


@dataclass
class Polygon:
    ''' A class to hold the polygon object '''
    vertices: List[LatLngPoint] # A minimum of three LatLngPoints

@dataclass
class Circle:
    ''' Hold the details of a circle object '''
    center: LatLngPoint 
    radius: Radius

@dataclass
class Altitude:
    ''' A class to hold altitude '''
    value:int
    reference:str
    units: str


@dataclass
class OperationalIntentReference:
    """Class for keeping track of an operational intent reference"""
    id: uuid.uuid4()

@dataclass
class Volume3D:
    '''A class to hold Volume3D objects'''
    outline_circle: Circle
    outline_polygon: Polygon
    altitude_lower: Altitude
    altitude_upper: Altitude


@dataclass
class Volume4D:
    '''A class to hold Volume4D objects'''
    volume: Volume3D
    time_start: StringBasedDateTime
    time_end: StringBasedDateTime

@dataclass
class OperationalIntentDetails:
    """Class for keeping track of an operational intent reference"""
    volumes: List[Volume4D]
    priority: int




class OperationCategory(str, enum.Enum):
    ''' A enum to hold all categories of an operation '''
    Vlos = 'vlos'
    Bvlos = 'bvlos'


class UASClass(str, enum.Enum):
    ''' A enum to hold all UAS Classes '''
    C0 = 'C0'
    C1 = 'C1'
    C2 = 'C2'
    C3 = 'C3'
    C4 = 'C4'

class TestResultState(str, enum.Enum):
    ''' A test is either pass or fail or could not be processed, currently not  '''
    Pass = 'Pass'
    Fail = 'Fail'
    

class IDTechnology(str, enum.Enum):
    ''' A enum to hold ID technologies for an operation '''
    Network = 'network'
    Broadcast = 'broadcast'

@dataclass
class FlightAuthorizationOperatorDataPayload:
    '''A class to hold information about Flight Authorization Test'''
    uas_serial_number: str
    operation_mode: Literal[OperationCategory.Vlos, OperationCategory.Bvlos]
    operation_category: str
    uas_class: Literal[UASClass.C0, UASClass.C1,
                       UASClass.C2, UASClass.C3, UASClass.C4, ]
    identification_technologies: Literal[IDTechnology.Network,
                                         IDTechnology.Broadcast]
    connectivity_methods: List[str]
    endurance_minutes: int
    emergency_procedure_url: str
    operator_id: str
@dataclass
class OperatorDataPayload:
    priority: int
    flight_authorisation: FlightAuthorizationOperatorDataPayload


@dataclass
class ExpectedTestResult:
    ''' A class to hold result of a test '''
    result: Literal[TestResultState.Pass, TestResultState.Fail]

