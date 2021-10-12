from django.core.exceptions import ObjectDoesNotExist
from gcs_operations.models import FlightLog, SignedFlightLog
from pki_framework import encrpytion_util
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.conf import settings
from pki_framework.models import AerobridgeCredential
import base64
import json

def get_SignedFlightLog(pk):
    created = 0
    try:        
        fl = FlightLog.objects.get(id=pk)              
        signed_fl, created = SignedFlightLog.objects.get_or_create(raw_flight_log= fl)
    except Exception as e:
        return None, created
    else:        
        return signed_fl, created

def sign_log(flightlog_id):

    status = 0
    signed_flight_log, created = get_SignedFlightLog(flightlog_id)        
    if signed_flight_log is None:
        status = 2
        return {"status":status, "signed_flight_log":signed_flight_log, "message":"Invalid Flight Log referenced in the request"}
    
    if created:                           
        # get the raw log
        flight_log = signed_flight_log.raw_flight_log
        flight_operation = flight_log.operation
        flight_plan = flight_operation.flight_plan
        raw_log = flight_log.raw_log
        
        minified_raw_log = json.dumps(raw_log , separators=(',', ':'))
        # sign the log and create a hash from the private key
        # IF log chaining is required
        #hs = hashlib.sha256(minified_raw_log.encode('utf-8')).hexdigest()
        # add signature to JSON
        operator = flight_log.operation.operator
        try: 
            credential_obj = AerobridgeCredential.objects.get(operator=operator, token_type = 1,association = 0, is_active = True)
        except ObjectDoesNotExist as oe:             
            signed_flight_log.delete()
            return {"status":status, "signed_flight_log":None, "message": "Credentials for the operator not found, please upload public and private keys for the operator of this operation via the Tokens Manager Interface"}

        
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')            
        f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
        operator_private_key_raw = f.decrypt(credential_obj.token).decode('utf-8')
        
        try:
            key = RSA.importKey(operator_private_key_raw)
            hasher = SHA256.new(minified_raw_log.encode('utf-8').strip())
            signer = PKCS1_v1_5.new(key)
            signature = signer.sign(hasher)
        except Exception as e:
            signed_flight_log.delete()
            return {"status":status, "signed_flight_log":None,  "message":"Error in signing your log, please contact your administrator"}
        else:
            sign = base64.b64encode(signature).decode()
            raw_log['signature'] = sign
            signed_flight_log.signed_log = raw_log
            signed_flight_log.save()            
            flight_operation.is_editable = False
            flight_operation.save()
            flight_log.is_editable = False
            flight_log.save()
            flight_plan.is_editable = False
            flight_plan.save()
        status = 1
        return {"status":status, "signed_flight_log":signed_flight_log,  "message":"Successfully signed raw log"}
    else:
        status = 2
        return {"status":status, "signed_flight_log":signed_flight_log, "message":"Signed flight logs already exist"}
