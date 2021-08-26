from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import FlightPlanListSerializer, FlightPlanSerializer, FlightOperationSerializer, FlightLogSerializer,FirmwareSerializer, FlightPermissionSerializer,CloudFileSerializer, SignedFlightLogSerializer
from .models import SignedFlightLog, Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission
from registry.models import Firmware
from gcs_operations.models import CloudFile
from pki_framework.models import AerobridgeCredential
from pki_framework import encrpytion_util
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from pki_framework.utils import requires_scopes
from digitalsky_provider.tasks import submit_flight_permission
import tempfile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import logging
import hashlib
import os, json
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from os import environ as env
from dotenv import load_dotenv, find_dotenv

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

load_dotenv(find_dotenv())
# Create your views here.


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class FirmwareList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class FirmwareDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightPlanList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FlightPlan.objects.all()
    serializer_class = FlightPlanListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightPlanDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FlightPlan.objects.all()
    serializer_class = FlightPlanSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightOperationList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FlightOperation.objects.all()
    serializer_class = FlightOperationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightOperationDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FlightOperation.objects.all()
    serializer_class = FlightOperationSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightLogList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FlightLog.objects.all()
    serializer_class = FlightLogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightLogDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FlightLog.objects.all()
    serializer_class = FlightLogSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightLogSign(APIView):
    

    def get_SignedFlightLog(self, pk):
        
        created = 0
        try:
            
            fl = FlightLog.objects.get(id=pk)              
            signed_fl, created = SignedFlightLog.objects.get_or_create(raw_flight_log= fl)
        except ObjectDoesNotExist:
            raise Http404
        except ObjectDoesNotExist:
            raise Http404
        else:
           
            return signed_fl, created

    def put(self, request, pk, format=None):
        signed_flight_log, created = self.get_SignedFlightLog(pk)
        
        if created:           
                
            # get the raw log
            flight_log = signed_flight_log.raw_flight_log
            raw_log = flight_log.raw_log
            raw_log_json = json.loads(raw_log)
            minified_raw_log = json.dumps(raw_log_json , separators=(',', ':'))
            # sign the log and create a hash from the private key
            # IF log chaining is required
            #hs = hashlib.sha256(minified_raw_log.encode('utf-8')).hexdigest()
            # add signature to JSON
            drone = flight_log.operation.drone
            
            credential_obj = AerobridgeCredential.objects.get(aircraft=drone, token_type = 1,association = 3, is_active = True)
            print(credential_obj)
            secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')            
            f = encrpytion_util.EncrpytionHelper(secret_key=secret_key)
            drone_private_key_raw = f.decrypt(credential_obj.token).decode()
            print(drone_private_key_raw)
            key = RSA.importKey(drone_private_key_raw,  passphrase='aerobridge')
            hasher = SHA256.new(minified_raw_log)
            signer = PKCS1_v1_5.new(key)
            signature = signer.sign(hasher)
            raw_log_json['signature'] = signature      
            signed_flight_log.signed_log = raw_log_json
            signed_flight_log.save()            

            # save URL
            serializer = SignedFlightLogSerializer(signed_flight_log, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Signed log object already exists"}, status=status.HTTP_409_CONFLICT)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class SignedFlightLogList(mixins.ListModelMixin,                  
                  generics.GenericAPIView):
    queryset = SignedFlightLog.objects.all()
    serializer_class = SignedFlightLogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class SignedFlightLogDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = SignedFlightLog.objects.all()
    serializer_class = SignedFlightLogSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        


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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class FlyDronePermissionApplicationSubmit(APIView):

    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    
    def post(self, request, permission_id,format=None):	
        permission = get_object_or_404(FlightPermission, pk=permission_id)
        submit_flight_permission.delay(permission_id = permission_id)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class CloudFileList(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = CloudFile.objects.all()
    serializer_class = CloudFileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class CloudFileDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = CloudFile.objects.all()
    serializer_class = CloudFileSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.write']), name='dispatch')
class CloudFileUpload(APIView):
    parser_classes = (MultiPartParser,)
    def put(self, request,document_type, format=None):
        
        if (document_type in ['logs', 'documents']):


            BUCKET_NAME = env.get("S3_BUCKET_NAME",0)
            endpoint_url = env.get('S3_ENDPOINT_URL',0)

            file_obj = request.FILES['file']
            for filename, file in request.FILES.items():
                file_name = request.FILES[filename].name
            friendly_name = request.POST.get("name")            
            file_type = request.POST.get("file_type")
            
            with tempfile.NamedTemporaryFile() as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
                f.flush()
                
                s3 = boto3.client('s3', region_name =env.get('S3_REGION_NAME',0), endpoint_url= endpoint_url, aws_access_key_id=env.get('S3_ACCESS_KEY',0),aws_secret_access_key=env.get('S3_SECRET_KEY',0))                
                
                try:
                    
                    s3.upload_fileobj(f, BUCKET_NAME, os.path.join(file_type, file_name))
                except NoCredentialsError as ne:                                        
                    return Response({"detail":"File not uploaded, problem  with Cloud Bucket credentials"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e: 
                    return Response({"detail":"File not uploaded, problem  with Cloud Bucket credentials"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    location = endpoint_url + '/' + file_type + file_name
                    cf = CloudFile(location= location,upload_type = file_type,  name = friendly_name)
                    cf.save()
                    return Response({'id':str(cf.id), 'name':cf.name,'location':location}, status=status.HTTP_201_CREATED)

        else:
                return Response({"detail":"File not uploaded, problem  with Cloud Bucket credentials"}, status=status.HTTP_400_BAD_REQUEST)