import dataclasses
from gcs_operations.models import FlightOperation, FlightPermission
import json
from dataclasses import asdict
import hashlib
from .data_definitions import PermissionObject, LatLng
from . import data_signer
from shapely.geometry import shape
from shapely.ops import unary_union
import logging
logger = logging.getLogger(__name__)

def issue_permission(flight_operation_id):

    ''' A class to issue permission JWS '''

    flight_operation = FlightOperation.objects.get(id = flight_operation_id)    
    ## Check airspace via the DSS
    flight_plan = flight_operation.flight_plan   
    airspace_clearance = True   
    # Generate Geocage and save it. 
    # Get Geojson
    geo_json = flight_plan.geo_json
    g_c = []
    shp_features = []
    for feature in geo_json['features']:
        shp_features.append(shape(feature['geometry']))
    combined_features = unary_union(shp_features)
    
    geo_cage = combined_features.minimum_rotated_rectangle
    for coord in list(geo_cage.exterior.coords):
        ll = LatLng(lat = float(coord[1]), lng = float(coord[0]))
        g_c.append(asdict(ll))
    
    if airspace_clearance: 
        status_code  = 'granted' 
        plan_file = flight_plan.plan_file_json
        h_digest = hashlib.sha256(json.dumps(plan_file).encode('utf-8')).hexdigest()        
        my_data_signer = data_signer.SigningHelper()    
        data_to_sign = PermissionObject(flight_operation_id= str(flight_operation.id), flight_plan_id= str(flight_plan.id), plan_file_hash = h_digest)    
        permission_payload = json.loads(json.dumps(dataclasses.asdict(data_to_sign)))        
        try:
            signed_json = my_data_signer.issue_jwt_permission(data_payload= permission_payload)    
        except Exception as e: 
            logger.error("Error in getting permission JSON from Auth server %s" % e)            
            signed_json = {'error': "Permission was granted but could not get a permission token"}

    else: 
        status_code  = 'denied'
        signed_json = {}

    if not signed_json: 
        status_code = 'denied'
        signed_json = {}
    
    flight_permission = FlightPermission(operation = flight_operation, token = signed_json,status_code=status_code, geo_cage = g_c)
    flight_permission.save()

    # Permission has been issued , lock the operation

    flight_operation.is_editable = False
    flight_operation.save()
    
    return {"flight_permission": flight_permission}