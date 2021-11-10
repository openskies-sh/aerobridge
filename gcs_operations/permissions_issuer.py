import dataclasses
from gcs_operations.models import FlightOperation, FlightPermission
import json
import hashlib
from data_signer import PermissionObject
from . import data_signer

def issue_permission(flight_operation_id):

    flight_operation = FlightOperation.objects.get(id = flight_operation_id)
    
    flight_plan = flight_operation.flight_plan
    # sign the flight plan 
    h_digest = hashlib.sha256(flight_plan.kml.encode('utf-8')).hexdigest()
    
    my_data_signer = data_signer.SigningHelper()
    
    data_to_sign = PermissionObject(flight_operation_id= str(flight_operation.id), flight_plan_id= str(flight_plan.id), flight_plan_kml_hash = h_digest)
    
    json_to_sign = json.dumps(dataclasses.asdict(data_to_sign))                    
    signed_json = my_data_signer.sign_json(data_to_sign= json_to_sign)    
    flight_permission = FlightPermission(operation = flight_operation, json = signed_json)
    flight_permission.save()
    
    return {"permission": flight_permission}