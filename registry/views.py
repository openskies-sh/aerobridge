# Create your views here.
from rest_framework import generics, mixins
from django.http import Http404

from rest_framework.response import Response
from .models import Firmware, Operator, Aircraft, Manufacturer, Pilot, Activity
from .serializers import (OperatorSerializer, AircraftSerializer, AircraftFullSerializer, ManufacturerSerializer,PilotSerializer,ActivitySerializer)
from gcs_operations.serializers import FirmwareSerializer

from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
# Create your views here.


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class ActivityList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all activities in the database
    """

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class ActivityDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Activity instance.
    """
    
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class PilotList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all pilots in the database
    """

    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class PilotDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Pilot instance.
    """
    
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class OperatorList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    List all operators, or create a new operator.
    """

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class OperatorDetail(mixins.RetrieveModelMixin,
                               generics.GenericAPIView):
    """
    Retrieve, update or delete a Operator instance.
    """

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class AircraftList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all aircrafts in the database
    """

    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class AircraftDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Aircraft.objects.all()
    serializer_class = AircraftFullSerializer
    
    def get_Aircraft(self, pk):
        try:
            a = Aircraft.objects.get(id=pk)
        except Aircraft.DoesNotExist:
            raise Http404
        else:
            return a

    def get(self, request, pk, format=None):
        aircraft = self.get_Aircraft(pk)
        serializer = AircraftFullSerializer(aircraft)
        return Response(serializer.data)



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class AircraftFirmwareDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Aircraft.objects.all()
    serializer_class = FirmwareSerializer
    
    def get_AircraftFirmware(self, flight_controller_id):
        try:
            a = Aircraft.objects.get(flight_controller_id=flight_controller_id)
        except Aircraft.DoesNotExist:
            raise Http404
        try:
            firmware = a.model.firmware
        except Firmware.DoesNotExist:
            raise Http404
        else:
            return firmware

    def get(self, request, flight_controller_id, format=None):
        firmware = self.get_AircraftFirmware(flight_controller_id = flight_controller_id)
        serializer = FirmwareSerializer(firmware)
        return Response(serializer.data)

@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class AircraftRFMDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Aircraft.objects.all()
    serializer_class = AircraftFullSerializer
    
    def get_Aircraft(self, flight_controller_id):
        try:
            a = Aircraft.objects.get(flight_controller_id=flight_controller_id)
        except Aircraft.DoesNotExist:
            raise Http404
        else:
            return a

    def get(self, request, flight_controller_id, format=None):
        aircraft = self.get_Aircraft(flight_controller_id = flight_controller_id)
        serializer = AircraftFullSerializer(aircraft)
        return Response(serializer.data)




@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class ManufacturerList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all aircrafts in the database
    """

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class ManufacturerDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    
    
