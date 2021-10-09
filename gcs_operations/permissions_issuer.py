from gcs_operations.models import FlightOperation
import json
import arrow
from pki_framework import encrpytion_util
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.conf import settings
from pki_framework.models import AerobridgeCredential
import base64

def issue_permission(flight_operation_id):

    flight_operation = FlightOperation.objects.get(id = flight_operation_id)  
    pass
    
#     # get the raw log
#     flight_plan = flight_operation.flight_plan
#     flight_operation = flight_log.operation
#     flight_plan = flight_operation.flight_plan
#     raw_log = flight_log.raw_log
#     raw_log_json = json.loads(raw_log)
#     minified_raw_log = json.dumps(raw_log_json , separators=(',', ':'))
#     # sign the log and create a hash from the private key
#     # IF log chaining is required
#     #hs = hashlib.sha256(minified_raw_log.encode('utf-8')).hexdigest()
#     # add signature to JSON
#     drone = flight_log.operation.drone
    
#     credential_obj = AerobridgeCredential.objects.get(aircraft=drone, token_type = 1,association = 3, is_active = True)
    
#     secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')            
#     f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
#     drone_private_key_raw = f.decrypt(credential_obj.token).decode('utf-8')
    
#     try:
#         key = RSA.importKey(drone_private_key_raw)
#         hasher = SHA256.new(minified_raw_log.encode('utf-8').strip())
#         signer = PKCS1_v1_5.new(key)
#         signature = signer.sign(hasher)
#     except Exception as e:
#         signed_flight_log.delete()
#     else:
#         sign = base64.b64encode(signature).decode()
#         raw_log_json['signature'] = sign
#         signed_flight_log.signed_log = raw_log_json
#         signed_flight_log.save()            
#         flight_operation.is_editable = False
#         flight_operation.save()
#         flight_log.is_editable = False
#         flight_log.save()
#         flight_plan.is_editable = False
#         flight_plan.save()
#     status = 1
#     return {"status":status, "signed_flight_log":signed_flight_log}
# else:
#     status = 2
#     return {"status":status, "signed_flight_log":signed_flight_log}
