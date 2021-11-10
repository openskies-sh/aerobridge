from dataclasses import dataclass
import uuid


@dataclass
class PermissionObject:
    '''A class to hold information about Flight Permission '''
    flight_plan_id: uuid
    flight_operation_id: uuid
    flight_plan_kml_hash: str
    