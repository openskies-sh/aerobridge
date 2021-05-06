from rest_framework import mixins
from rest_framework import generics
from .serializers import TransactionSerializer, FlightPlanListSerializer, FlightPlanSerializer, FlightOperationListSerializer, FlightOperationSerializer, FlightLogSerializer,FirmwareSerializer
from .models import Transaction, FlightOperation, FlightPlan, FlightLog, FlightPermission
from registry.models import Firmware
from django.utils.decorators import method_decorator

from pki_framework.utils import requires_scopes
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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
