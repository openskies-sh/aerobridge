from rest_framework import mixins
from rest_framework import generics
from .serializers import FlightPlanListSerializer, FlightPlanSerializer, FlightOperationSerializer, FlightLogSerializer,FirmwareSerializer, FlightPermissionSerializer
from .models import Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission
from registry.models import Firmware
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from pki_framework.utils import requires_scopes
from digialsky_provider.tasks import submit_flight_permission
# Create your views here.

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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class FlightOperationDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = FlightOperation.objects.all()
    serializer_class = FlightOperationSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
