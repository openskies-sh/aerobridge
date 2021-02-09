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
from .models import DigitalSkyLog, AircraftRegister
from gcs_operations.models import FlightOperation, UINApplication, FlightLog, Transaction, FlightPermission

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from registry.models import Aircraft
from pki_framework.utils import requires_scopes, BearerAuth
from .serializers import DigitalSkyLogSerializer, AircraftRegisterSerializer
import json
from gcs_operations.serializers import FlightPermissionSerializer, UINApplicationSerializer, FlightLogSerializer
from rest_framework.response import Response
# Create your views here.


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class PingView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        return Response(json.dumps({"message":"pong"}), status=status.HTTP_200_OK)



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class UINApplicationList(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = UINApplication.objects.all()
    serializer_class = UINApplicationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class UINApplicationDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = UINApplication.objects.all()
    serializer_class = UINApplicationSerializer


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class SubmitUINApplication(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = UINApplication.objects.all()
    serializer_class = UINApplicationSerializer

    def post(self, request, uin_application_id, format=None):
        
        uin_application = get_object_or_404(UINApplication, pk=uin_application_id)
        drone = uin_application.drone

        t = Transaction(drone = drone, prefix="uin_application")
        t.save()
        counter = uin_application.counter
        operator = uin_application.operator
        headers = {'content-type': 'application/json'}

        securl = os.environ.get('DIGITAL_SKY_URL')  + '/api/applicationForm/uinApplication'
        
        payload = {"feeDetails":"bank transfer","droneTypeId":drone.sub_category,"operatorDroneId":str(drone.id),"manufacturer":drone.manufacturer.common_name,"manufacturerAddress":drone.manufacturer.address,"manufacturerDesignation":drone.manufacturer.role,"manufacturerNationality":drone.manufacturer.country,"modelName":drone.model,"modelNo":drone.master_series,"serialNo":drone.esn,"dateOfManufacture":drone.manufactured_at,"wingType":drone.sub_category,"maxTakeOffWeight":drone.max_certified_takeoff_weight,"maxHeightAttainable":drone.max_height_attainable,"compatiblePayload":"","droneCategoryType":drone.category,"purposeOfOperation":"Surveying","engineType":drone.engine.type,"enginePower":drone.engine.power,"engineCount":drone.engine.count,"fuelCapacity":drone.fuel_capacity,"propellerDetails":drone.engine.propellor,"maxEndurance":drone.max_endurance,"maxRange":drone.max_range,"maxSpeed":drone.max_speed,"maxHeightOfOperation":"100","dimensions":{"length":drone.dimension_length,"breadth":drone.dimension_breadth,"height":drone.dimension_height},"ownerName":drone.operator.name,"ownerPhone":drone.operator.phone_number,"ownerEmail":drone.operator.email,"ownerAddress":drone.operator.get_address,"uinNumber":"TBC"}
        r = requests.post(securl, data= json.dumps(payload), headers=headers)

        now = datetime.datetime.now()
        uin_response = json.loads(r.text)

        if r.status_code == 200:
            if uin_response['status'] == 'APPROVED':
                uin_response.is_successful = True
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = uin_response['code'], timestamp = now)
            ds_log.save()
            return Response(status=status.HTTP_200_OK)
        else:
            ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = uin_response['code'], timestamp = now)
            ds_log.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class AircraftRegisterList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = AircraftRegister.objects.all()
    serializer_class = AircraftRegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     aircrafts = Aircraft.objects.all()
    #     for aircraft in aircrafts:
    #         ar, created = AircraftRegister.objects.get_or_create(drone = aircraft)
        
    #     aircraftregister = AircraftRegister.objects.all()
    #     serializer = AircraftRegisterSerializer(aircraftregister, many=True)
    #     return JsonResponse(serializer.data, safe=False)


    # def put(self, request, format=None):
    #     serializer = AircraftRegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class AircraftRegisterDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    queryset = AircraftRegister.objects.all()
    serializer_class = AircraftRegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class RegisterDrone(mixins.CreateModelMixin, generics.GenericAPIView):

    """
    Execute Drone registration

    """
    serializer_class = DigitalSkyLogSerializer
    
    def post(self, request, drone_id,format=None):	
        aircraft_register = get_object_or_404(AircraftRegister, drone=drone_id)
        drone = aircraft_register.drone        
        operator = get_object_or_404(Operator, aircraft=drone)
        t = Transaction(drone = drone, prefix="registration")
        t.save()
        
        if aircraft_register.is_signed:
                
            securl = os.environ.get('DIGITAL_SKY_URL') + '/api/droneDevice/register/<manufacturerBusinessIdentifier>'
            headers = {'content-type': 'application/json'}

            drone_details ={"droneTypeId": drone.type_id, "version": drone.version, "txn":t.get_txn_id(), "deviceID":drone.device_id, "deviceModelId": drone.device_model_id, "operatorBusinessIdentifier": operator.company_number}

            payload = {"drone": json.dumps(drone_details), "signature":aircraft_register.signature, "digitalCertificate":aircraft_register.certificate}

            r = requests.post(securl, data= json.dumps(payload), headers=headers)
            now = datetime.datetime.now()
            registration_response = json.loads(r.text)
            if (r.status_code == 201):
                # create a entry 
                ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = registration_response['code'], timestamp = now)
                ds_log.save()
                drone.is_registered = True
                drone.save()
                return Response(json.dumps({'message':'success', 'digital_sky_log_id':str(ds_log.id)}), status=status.HTTP_201_CREATED)
            else:
                ds_log = DigitalSkyLog(txn = t, response = r.text, response_code = registration_response['code'], timestamp = now)
                ds_log.save()
                return Response(json.dumps({'message':'error',' digital_sky_log_id':str(ds_log.id)}),status=status.HTTP_400_BAD_REQUEST)
        
        else: 
            message = {"message": "Please sign the drone details first using a DSC token."}
            return Response(json.dumps(message), status=status.HTTP_400_BAD_REQUEST)


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
