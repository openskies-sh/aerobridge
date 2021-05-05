import requests
import os, json
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
import datetime
from rest_framework import status
from django.utils.decorators import method_decorator
from .models import DigitalSkyLog, AircraftRegister
from gcs_operations.models import FlightOperation,  FlightLog, Transaction, FlightPermission

from pki_framework.utils import requires_scopes, BearerAuth
from .serializers import DigitalSkyLogSerializer, AircraftRegisterSerializer
import json
from gcs_operations.serializers import FlightPermissionSerializer, FlightLogSerializer
from rest_framework.response import Response
# Create your views here.



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class FlyDronePermissionApplicationList(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class FlyDronePermissionApplicationDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def post(self, request, operation_id,format=None):	
        operation = get_object_or_404(FlightOperation, pk=operation_id)
        drone = operation.Aircraft
        t = Transaction(drone = drone, prefix="permission")
        t.save()
        permission = FlightPermission(operation= operation)
        permission.save()
        
        flight_plan = operation.flight_plan
        drone = operation.drone_details
        
        payload = {"pilotBusinessIdentifier":drone.operator_business_id,"flyArea":flight_plan.details,"droneId":str(drone.id),"payloadWeightInKg":drone.max_certified_takeoff_weight *1.0, "payloadDetails":"test","flightPurpose":operation.purpose,"typeOfOperation":operation.type_of_operation,"flightTerminationOrReturnHomeCapability":operation.flight_termination_or_return_home_capability,"geoFencingCapability":operation.geo_fencing_capability,"detectAndAvoidCapability":operation.detect_and_avoid_capability,"selfDeclaration":"true","startDateTime":flight_plan.start_datetime,"endDateTime":flight_plan.end_datetime,"recurringTimeExpression":operation.recurring_time_expression,"recurringTimeDurationInMinutes":operation.recurring_time_duration,"recurringTimeExpressionType":"CRON_QUARTZ"}
        
        headers = {'content-type': 'application/json'}

        securl = os.environ.get('DIGITAL_SKY_URL')  + '/api/applicationForm/flyDronePermissionApplication'
        r = requests.post(securl, data= json.dumps(payload), headers=headers)

        now = datetime.datetime.now()
        permission_response = json.loads(r.text)

        if r.status_code == 200:
            if permission_response['status'] == 'APPROVED':
                permission.is_successful = True
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            ds_log.save()
            return Response(status=status.HTTP_200_OK)
        else:
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            ds_log.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class FlyDronePermissionApplicationFlightLog(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class DownloadFlyDronePermissionArtefact(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def get(self, request, permission_id, format=None):
        permission = get_object_or_404(FlightPermission, pk=permission_id)
        
            
        try:
            assert permission.is_successful
        except AssertionError as ae: 
            message ={"status":0, "message":"No permission for operation, please get permission first"}
            return Response(json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
        
        if permission.artefact != "": 
            return Response(permission.artefact, status=status.HTTP_200_OK)
        else:
            # there is no permission artefact 
            # download and save it. 
            
            headers = {'content-type': 'application/json'}
            securl = os.environ.get('DIGITAL_SKY_URL')+ '/api/applicationForm/flyDronePermissionApplication/'+str(permission.id)+'/document/permissionArtifact'
            auth = BearerAuth(os.environ.get('BEARER_TOKEN', ""))
            r = requests.get(securl,auth = auth,  headers=headers)
            now = datetime.datetime.now()
            
            if r.status_code == 200:
            
                ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
                permission.arefact = r.text()
                permission.save()
                msg = {"status":1, "aretefact": r.text()}
                return Response(json.dumps(msg), status=status.HTTP_200_OK)
            else:
                ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
                ds_log.save()
                return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class LogList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = DigitalSkyLog.objects.all()
    serializer_class = DigitalSkyLogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class LogDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = DigitalSkyLog.objects.all()
    serializer_class = DigitalSkyLogSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class SubmitSignedFlightLog(mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = FlightLog.objects.all()
    serializer_class = FlightLogSerializer


    def post(self, request, operation_id, format=None):
        operation = get_object_or_404(FlightOperation, pk=operation_id)
        permission = get_object_or_404(FlightPermission, operation= operation)
        flight_log = FlightLog.objects.get_object_or_404(operation = operation)
        
        drone = operation.aircraft
               
        t = Transaction(drone = drone, prefix="flight_log_submission")
        t.save()
        
        log_json = {"PermissionArtefact":{"type":"string","title":"Permission Artefact ID","description":str(permission.id)},"previous_log_hash":flight_log.signed_log,"LogEntries":flight_log.raw_log}
        
        headers = {'content-type': 'application/json'}

        try:
            assert flight_log.is_submitted == False
        except AssertionError as ae: 
            message ={"status":0, "message":"Flight log already submitte"}
            return Response(json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
    
        headers = {'content-type': 'application/json'}
        securl = os.environ.get('DIGITAL_SKY_URL')+ '/api/applicationForm/flyDronePermissionApplication/'+str(permission.id)+'/document/flightLog'
        
        
        auth = BearerAuth(os.environ.get('BEARER_TOKEN', ""))
        r = requests.get(securl,auth = auth,  headers=headers)
        now = datetime.datetime.now()
        
        if r.status_code == 200:
        
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            permission.arefact = r.text()
            permission.save()
            msg = {"status":1, "flight_log_submission": r.text()}
            return Response(json.dumps(msg), status=status.HTTP_200_OK)
        else:
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = permission_response['code'], timestamp = now)
            ds_log.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)
