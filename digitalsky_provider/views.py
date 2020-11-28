from django.shortcuts import render

import requests
import os, json
from rest_framework import mixins
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import jwt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from gcs_operations.models import Transaction
from .models import DigitalSkyLog
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from registry.models import Aircraft
from pki_framework.utils import requires_scopes
from .serializers import DigitalSkyLogSerializer

# Create your views here.



@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class RegisterDrone(mixins.CreateModelMixin, generics.GenericAPIView):

    """
    Execute Drone registration

    """
    serializer_class = DigitalSkyLogSerializer
    def post(self, request, drone_id,format=None):		

        drone = get_object_or_404(Aircraft, pk=drone_id)
        t = Transaction(drone = Aircraft, prefix="registration")
        t.save()

        private_key = os.environ.get('PRIVATE_KEY')
        certificate = os.environ.get('X509_CERTIFICATE')
        private_key = private_key.replace('-----BEGIN ENCRYPTED PRIVATE KEY-----goo', '')
        private_key = private_key.replace('-----END ENCRYPTED PRIVATE KEY-----', '')

    
        priv_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
        
        drone_details ={"droneTypeId": drone.type_id, "version": drone.version, "txn":t.get_txn_id(), "deviceID":drone.device_id, "deviceModelId": drone.device_model_id, "operatorBusinessIdentifier": drone.operator_business_id}
        drone_details_string = json.dumps(drone_details)
        drone_details_bytes = drone_details_string.encode("utf-8") 


        signature = priv_key.sign(drone_details_bytes,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        # Sign the drone details
        signature = b64encode(signature)
        
        securl = os.environ.get('DIGITAL_SKY_URL')
        headers = {'content-type': 'application/json'}

        drone_details ={"droneTypeId": drone.type_id, "version": drone.version, "txn":t.get_txn_id(), "deviceID":drone.device_id, "deviceModelId": drone.device_model_id, "operatorBusinessIdentifier": drone.operator_business_id}


        payload = {"drone": json.dumps(drone_details), "signature":signature, "digitalCertificate":certificate}

        r = requests.post(securl, data= json.dumps(payload), headers=headers)

        if r.status_code == 201:
            registration_response = json.loads(r.text)
            # create a entry 
            ds_log = DigitalSkyLog(txn = t, response_code = registration_response['code'], timestamp = datetime.datetime.now())
            ds_log.save()
            drone.is_registered = True
            drone.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
