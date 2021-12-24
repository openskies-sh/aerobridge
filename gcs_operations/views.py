from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import FlightPlanListSerializer, FlightPlanSerializer, FlightOperationSerializer, FlightLogSerializer,FirmwareSerializer, FlightPermissionSerializer,CloudFileSerializer, SignedFlightLogSerializer, FlightOperationPermissionSerializer
from .models import SignedFlightLog, Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission
from registry.models import Firmware
from gcs_operations.models import CloudFile
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from pki_framework.utils import requires_scopes
from . import permissions_issuer
import tempfile

import logging
from rest_framework import serializers
import arrow
import os
import boto3
from . import data_signer
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from os import environ as env
from dotenv import load_dotenv, find_dotenv


logger = logging.getLogger(__name__)

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
        logger.error("Error in S3 upload %s" %e)
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


@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightPlanList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = FlightPlan.objects.all()
    serializer_class = FlightPlanSerializer

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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
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
class FlightPermissionApplicationGenerate(APIView):

    def put(self, request, operation_id,format=None):	
        flight_operation = get_object_or_404(FlightOperation, pk=operation_id)       

        permission = FlightPermission.objects.filter(operation = flight_operation).exists()
        if permission:
            f_p = FlightPermission.objects.get(operation = flight_operation)            
        else:
            now = arrow.now()
            start_datetime = flight_operation.start_datetime
            operation_start_time_delta = start_datetime - now         

            if not (operation_start_time_delta.total_seconds() < 3600 and operation_start_time_delta.total_seconds() > 60):
                raise serializers.ValidationError("Cannot issue permissions for operations whose start time is in the past or more than a hour from now")
            
            f_permission = permissions_issuer.issue_permission(flight_operation_id = flight_operation.id)            
            f_p = f_permission['flight_permission']            
        if not f_p: 
            raise serializers.ValidationError("Error in creating / issuing a permission object, please see server logs")
        else:         
            serializer = FlightPermissionSerializer(f_p)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
                

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
    
    def put(self, request, pk, format=None):
        sign_result = data_signer.sign_log(pk)
        if sign_result['status'] ==1:
            signed_flight_log = sign_result['signed_flight_log']
            serializer = SignedFlightLogSerializer(signed_flight_log)
            return Response(serializer.data)

        elif sign_result['status'] ==2:
            return Response({"message":"Signed log object already exists"}, status=status.HTTP_409_CONFLICT)

        else:
            return Response({"message":"No flight Log found to sign"}, status=status.HTTP_404_NOT_FOUND)

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
class FlightPermissionApplicationList(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
@method_decorator(requires_scopes(['aerobridge.read','aerobridge.write']), name='dispatch')
class FlightPermissionApplicationDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = FlightPermission.objects.all()
    serializer_class = FlightPermissionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
        
        if document_type in ['photos','documents']:

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
                    logger.error("S3 Error, credentails not found / supplied %s" % ne)                                   
                    return Response({"detail":"File not uploaded, problem  with Cloud Bucket credentials"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e: 
                    logger.error("S3 Error during upload %s" % e)   
                    return Response({"detail":"File not uploaded, see your administrator for logs / resolving this issue"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    location = endpoint_url + '/' + file_type + file_name
                    cf = CloudFile(location= location,upload_type = file_type,  name = friendly_name)
                    cf.save()
                    return Response({'id':str(cf.id), 'name':cf.name,'location':location}, status=status.HTTP_201_CREATED)

        else:
                return Response({"detail":"File not uploaded, you can only choose to upload in the documents subfolder."}, status=status.HTTP_400_BAD_REQUEST)
