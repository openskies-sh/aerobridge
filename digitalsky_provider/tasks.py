
from celery.decorators import task
from gcs_operations.models import FlightPermission, Transaction, FlightLog
from digitalsky_provider.models import DigitalSkyLog
from .utils import ArtefactRequest, FlightLogPayload
import os
import uuid
from io import BytesIO
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
            
@task(name='submit_flight_log')
def submit_flight_log(flight_log_id):  
    ''' This method submits the flight log zip file added to Digital Sky '''   
    
    flight_log = FlightLog.objects.get(id = flight_log_id) # Get the flight log object
    operation = flight_log.operation # Get the operation
    permission = FlightPermission.objects.get(operation = operation) # Get the associated permission
    drone = operation.Aircraft # Get the transaction 
    
    permission_artefact_id = permission.id # get the id of the permission artefact TODO: This is not clear but can be the ID provided by DigitalSky
    signed_log_url = flight_log.signed_log # Get the URl of the signed log 
    
    log_response = requests.get(signed_log_url)
    if log_response.status == 200:
        flight_log_file = BytesIO(log_response.read())
        flight_log_file.seek(0, os.SEEK_END)

        
        uin = str(uuid.uuid4()) # TODO: Figure out how to get UIN in Aerobridge
        
        flp = FlightLogPayload(uin = uin, permissionArtefactId = permission_artefact_id, flightLogFile = flight_log_file)
        payload = json.dumps(flp)
        
    
        securl = os.getenv('DIGITAL_SKY_URL')  + '/digital-sky/public/rpas/flight-logs/upload'
        t = Transaction(drone = drone, prefix="log_upload")
        t.save()

        r = requests.post(securl, data=payload)
        now = datetime.datetime.now()
        flight_log_upload_response = json.loads(r.text)
        if flight_log_upload_response.status_code == 201:
            if flight_log_upload_response['status'] == 'SUBMITTED':
                flight_log.is_submitted = True
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = flight_log_upload_response['code'], timestamp = now)
            ds_log.save()            
        else:
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = flight_log_upload_response['code'], timestamp = now)
            ds_log.save()
    
    
        