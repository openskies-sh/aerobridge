
from celery.decorators import task
from gcs_operations.models import FlightPermission, Transaction
from digitalsky_provider.models import DigitalSkyLog
from . utils import ArtefactRequest
import os
import json, requests
import datetime
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


@task(name='submit_flight_permission')
def submit_flight_permission(permission_id):        
        permission = FlightPermission.objects.get(id=permission_id)
        operation = permission.operation
        drone = operation.Aircraft
        t = Transaction(drone = drone, prefix="permission")
        t.save()
        permission = FlightPermission(operation= operation)
        permission.save()
        
        flight_plan = operation.flight_plan
        drone = operation.drone_details
        ar = ArtefactRequest(id =str(flight_plan.id))
        payload = json.dumps(ar)
        headers = {'content-type': 'application/json'}

        securl = os.getenv('DIGITAL_SKY_URL')  + 'digital-sky/public/rpa/permissionArtifact'
        
        r = requests.post(securl, json=payload, headers=headers)

        now = datetime.datetime.now()
        permission_response = json.loads(r.text)

        if r.status_code == 200:
            if permission_response['status'] == 'APPROVED':
                permission.is_successful = True
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            ds_log.save()            
        else:
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            ds_log.save()