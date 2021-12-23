import dataclasses
from gcs_operations.models import FlightOperation, FlightPermission
import json
import hashlib
from .data_definitions import PermissionObject
from . import data_signer
import logging
logger = logging.getLogger(__name__)

def issue_permission(flight_operation_id):

    ''' A class to issue permission JWS '''

    flight_operation = FlightOperation.objects.get(id = flight_operation_id)    
    ## Check airspace via the DSS
    airspace_clearance = True   
    
    if airspace_clearance: 
        status_code  = 'granted'
        flight_plan = flight_operation.flight_plan    
        plan_file = flight_plan.plan_file_json
        h_digest = hashlib.sha256(json.dumps(plan_file).encode('utf-8')).hexdigest()        
        my_data_signer = data_signer.SigningHelper()    
        data_to_sign = PermissionObject(flight_operation_id= str(flight_operation.id), flight_plan_id= str(flight_plan.id), plan_file_hash = h_digest)    
        permission_payload = json.loads(json.dumps(dataclasses.asdict(data_to_sign)))        
        try:
            signed_json = my_data_signer.sign_json(data_payload= permission_payload)    
        except Exception as e: 
            logger.error("Error in getting permission JSON from Auth server %s" % e)            
            signed_json = {'error': "Permission was granted but could not sign permission object"}
    else: 
        status_code  = 'denied'
        signed_json = {}

    if not signed_json: 
        status_code = 'denied'
        signed_json = {}
    
    flight_permission = FlightPermission(operation = flight_operation, token = signed_json,status_code=status_code)
    flight_permission.save()
    # Permission has been issued , lock the operation

    flight_operation.is_editable = False
    flight_operation.save()
    
    return {"flight_permission": flight_permission}