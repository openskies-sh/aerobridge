import logging
from django.core.exceptions import ObjectDoesNotExist
from gcs_operations.models import FlightLog, SignedFlightLog
from pki_framework import encrpytion_util
from Crypto.Hash import SHA256

import json
import requests


from os import environ as env
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

class SigningHelper():
    ''' A class to sign data using Flight Passport '''
    def __init__(self):
        
        self.signing_client_id = env.get('FLIGHT_PASSPORT_SIGNING_CLIENT_ID')
        self.signing_client_secret = env.get('FLIGHT_PASSPORT_SIGNING_CLIENT_SECRET')
        
        
    def sign_json(self, data_to_sign):      
        
        signed_json = None
        try:
            assert self.signing_client_id is not None
            assert self.signing_client_secret is not None
        except AssertionError as ae:
            logger.warn("Client ID and Secret not set in the environment")
        else:            
            payload = {"client_id": env.get('FLIGHT_PASSPORT_SIGNING_CLIENT_ID'),"client_secret": env.get('FLIGHT_PASSPORT_SIGNING_CLIENT_SECRET'),"raw_data":data_to_sign }

            url = env.get('FLIGHT_PASSPORT_SIGNING_URL')
            signed_json = requests.post(url, json = payload)
            signed_json = signed_json.json() 
            
        return signed_json


def signed_flight_log_exists(flight_log):
    
    return SignedFlightLog.objects.filter(raw_flight_log= flight_log).exists()


def sign_log(flightlog_id):
    status = 0
    try:       
         
        flight_log = FlightLog.objects.get(id=flightlog_id)    
    except ObjectDoesNotExist as oe:        
        logger.warning("Flight Log Object Does not exist: %s" % oe)
        status = 2
        return {"status":status, "signed_flight_log":None, "message":"Invalid Flight Log referenced in the request"}
    
    sfl_exists = signed_flight_log_exists(flight_log = flight_log)
    
    if sfl_exists: # Signed flight log does not exist        
        signed_flight_log = SignedFlightLog.objects.get(raw_flight_log= flight_log)        
        status = 2
        return {"status":status, "signed_flight_log":signed_flight_log, "message":"Signed flight log already exist for that operation"}

    else:                           
        
        # get the raw log
        
        flight_operation = flight_log.operation
        flight_plan = flight_operation.flight_plan
        raw_log = flight_log.raw_log
        
        minified_raw_log = json.dumps(raw_log , separators=(',', ':'))
        # sign the log and create a hash from the private key
        # IF log chaining is required
        #hs = hashlib.sha256(minified_raw_log.encode('utf-8')).hexdigest()
        # add signature to JSON
        
        my_signing_helper = SigningHelper()
        try:        
            hasher = SHA256.new(minified_raw_log.encode('utf-8').strip())
            json_to_sign = {"raw_log_id": str(flight_log.id), "digest":hasher.hexdigest()}
            signed_data = my_signing_helper.sign_json(json_to_sign)
            if signed_data is None:
                raise Exception
        except Exception as e:
            logger.error("Error in signing JSON %s" % e)
            status = 2
            return {"status":status, "signed_flight_log":None,  "message":"Error in signing your log, please contact your administrator"}
        else:            
            raw_log['signature'] = signed_data
            sfl = SignedFlightLog(raw_flight_log = flight_log, signed_log= raw_log)
            sfl.save()
            flight_operation.is_editable = False
            flight_operation.save()
            flight_log.is_editable = False
            flight_log.save()
            flight_plan.is_editable = False
            flight_plan.save()
        status = 1
        return {"status":status, "signed_flight_log":sfl,  "message":"Successfully signed raw log"}
    