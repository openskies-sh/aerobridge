from dataclasses import dataclass
import uuid
import enum
from typing import Literal,List
import arrow


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
