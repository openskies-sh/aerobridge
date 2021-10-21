from io import BufferedIOBase
from pki_framework.models import AerobridgeCredential
from django.shortcuts import render

from registry.models import Authorization, Person, Address, Operator, Aircraft, Manufacturer, Firmware, Contact, Pilot, Engine, Activity
from registry.models import AircraftDetail as ad
from registry.serializers import AircraftFullSerializer
from gcs_operations.models import CloudFile, FlightOperation, FlightLog, FlightPlan, FlightPermission, SignedFlightLog
from gcs_operations.serializers import CloudFileSerializer, FlightLogSerializer, SignedFlightLogSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic import TemplateView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import PersonSerializer, AddressSerializer, OperatorSerializer, AircraftSerializer, ManufacturerSerializer, FirmwareSerializer, ContactSerializer, PilotSerializer, EngineSerializer, ActivitySerializer, AuthorizationSerializer, AircraftDetailSerializer
from pki_framework.serializers import AerobridgeCredentialSerializer, AerobridgeCredentialGetSerializer
# from pki_framework.forms import TokenCreateForm
from pki_framework import encrpytion_util
from jetway.pagination import StandardResultsSetPagination
from rest_framework.generics import DestroyAPIView
from .forms import PersonCreateForm, AddressCreateForm, OperatorCreateForm , AircraftCreateForm, ManufacturerCreateForm, FirmwareCreateForm, FlightLogCreateForm, FlightOperationCreateForm, AircraftDetailCreateForm, FlightPlanCreateForm,  ContactCreateForm, PilotCreateForm,EngineCreateForm, ActivityCreateForm,CustomCloudFileCreateForm, AuthorizationCreateForm, TokenCreateForm
from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
from gcs_operations.serializers import FlightPlanSerializer, FlightOperationSerializer, FlightPermissionSerializer, FlightLogSerializer
import tempfile
from rest_framework.parsers import MultiPartParser
import boto3
from gcs_operations import log_signer, permissions_issuer
from botocore.exceptions import ClientError
from django.core.exceptions import ObjectDoesNotExist
from botocore.exceptions import NoCredentialsError
from os import environ as env
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class HomeView(TemplateView):
    template_name = 'launchpad/basecamp.html'

class DigitalSkyReadFirst(TemplateView):
    template_name = 'launchpad/digital_sky/digitalsky_read_first.html'
    
class FlightPermissionsReadFirst(TemplateView):
    template_name = 'launchpad/flight_permission/flight_permissions_read_first.html'

### Person Views 
class PeopleList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/person/person_list.html'

    def get(self, request):
        queryset = Person.objects.all()
        return Response({'people': queryset})
    
class PersonUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/person/person_update.html'

    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        serializer = PersonSerializer(person)
        return Response({'serializer': serializer, 'person': person})

    def post(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        serializer = PersonSerializer(person, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'person': person,'errors':serializer.errors})
        serializer.save()
        return redirect('people-list')


class PersonDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/person/person_detail.html'

    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        serializer = PersonSerializer(person)
        return Response({'serializer': serializer, 'person': person})


class PersonCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': PersonCreateForm()}
        return render(request, 'launchpad/person/person_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PersonCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('people-list')

        return render(request, 'launchpad/person/person_create.html', context)
  
    
### Address Views
    
    
class AddressList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/address/address_list.html'

    def get(self, request):
        queryset = Address.objects.all()
        return Response({'addresses': queryset})
    
class AddressDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/address/address_detail.html'

    def get(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address)
        return Response({'serializer': serializer, 'address': address})

    def post(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'address': address,'errors':serializer.errors})
        serializer.save()
        return redirect('addresses-list')

class AddressCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AddressCreateForm()}
        return render(request, 'launchpad/address/address_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AddressCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('addresses-list')

        return render(request, 'launchpad/address/address_create.html', context)
  

### Operator Views
    
    
class OperatorList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/operator/operator_list.html'

    def get(self, request):
        queryset = Operator.objects.all()
        return Response({'operators': queryset})
    
class OperatorDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/operator/operator_detail.html'

    def get(self, request, operator_id):
        operator = get_object_or_404(Operator, pk=operator_id)
        serializer = AircraftSerializer(operator)
        return Response({'serializer': serializer, 'operator': operator})


class OperatorUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/operator/operator_update.html'

    def get(self, request, operator_id):
        operator = get_object_or_404(Operator, pk=operator_id)
        serializer = OperatorSerializer(operator)
        return Response({'serializer': serializer, 'operator': operator})

    def post(self, request, operator_id):
        operator = get_object_or_404(Operator, pk=operator_id)
        serializer = OperatorSerializer(operator, data=request.data)
        if not serializer.is_valid():
            
            return Response({'serializer': serializer, 'operator': operator, 'errors': serializer.errors})
        serializer.save()
        return redirect('operators-list')

class OperatorCreateView(CreateView):
    template_name = 'launchpad/operator/operator_create.html'
    form_class = OperatorCreateForm
    model= Operator
    
    def post(self, request, *args, **kwargs):
        form = OperatorCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('operators-list')

        return render(request, 'launchpad/operator/operator_create.html', context)
  

### Contact Views
    
class ContactsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/contact/contact_list.html'

    def get(self, request):
        queryset = Contact.objects.all()
        return Response({'contacts': queryset})
    
class ContactsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/contact/contact_detail.html'

    def get(self, request, contact_id):
        contact = get_object_or_404(Contact, pk=contact_id)
        serializer = ContactSerializer(contact)
        
        return Response({'serializer': serializer, 'contact': contact})

class ContactsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/contact/contact_update.html'

    def get(self, request, contact_id):
        contact = get_object_or_404(Contact, pk=contact_id)
        serializer = ContactSerializer(contact)
        
        return Response({'serializer': serializer, 'contact': contact})


class ContactsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ContactCreateForm()}
        return render(request, 'launchpad/contact/contact_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('contacts-list')

        return render(request, 'launchpad/contact/contact_create.html', context)
  
### Flight Pilot Views
    
class PilotsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/pilot/pilot_list.html'

    def get(self, request):
        queryset = Pilot.objects.all()
        return Response({'pilots': queryset})
    
class PilotsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/pilot/pilot_detail.html'

    def get(self, request, pilot_id):
        pilot = get_object_or_404(Pilot, pk=pilot_id)
        serializer = PilotSerializer(pilot)
        return Response({'serializer': serializer, 'pilot': pilot})


class PilotsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/pilot/pilot_update.html'

    def get(self, request, pilot_id):
        pilot = get_object_or_404(Pilot, pk=pilot_id)
        serializer = PilotSerializer(pilot)
        return Response({'serializer': serializer, 'pilot': pilot})


class PilotsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': PilotCreateForm()}
        return render(request, 'launchpad/pilot/pilot_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PilotCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('pilots-list')

        return render(request, 'launchpad/pilot/pilot_create.html', context)
  

### Authorizationa Views
    
class AuthorizationsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/authorization/authorization_list.html'

    def get(self, request):
        queryset = Authorization.objects.all()
        return Response({'authorizations': queryset})
    
class AuthorizationsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/authorization/authorization_detail.html'

    def get(self, request, authorization_id):
        authorization = get_object_or_404(Authorization, pk=authorization_id)
        serializer = AuthorizationSerializer(authorization)
        return Response({'serializer': serializer, 'authorization': authorization})

class AuthorizationsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/authorization/authorization_update.html'

    def get(self, request, authorization_id):
        authorization = get_object_or_404(Authorization, pk=authorization_id)
        serializer = AuthorizationSerializer(authorization)
        return Response({'serializer': serializer, 'authorization': authorization})

    def post(self, request, authorization_id):
        authorization = get_object_or_404(Authorization, pk=authorization_id)
        serializer = AuthorizationSerializer(authorization, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'authorization': authorization,'errors':serializer.errors})
        serializer.save()
        return redirect('authorizations-list')


class AuthorizationsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AuthorizationCreateForm()}
        return render(request, 'launchpad/authorization/authorization_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AuthorizationCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('authorizations-list')

        return render(request, 'launchpad/authorization/authorization_create.html', context)
  
    


### Activites Views
    
class ActivitiesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/activity/activity_list.html'

    def get(self, request):
        queryset = Activity.objects.all()
        return Response({'activities': queryset})
    
class ActivitiesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/activity/activity_detail.html'

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity)
        return Response({'serializer': serializer, 'activity': activity})

class ActivitiesUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/activity/launchpad/activity/activity_update.html'

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity)
        return Response({'serializer': serializer, 'activity': activity})

    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'activity': activity,'errors':serializer.errors})
        serializer.save()
        return redirect('activities-list')


class ActivitiesCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ActivityCreateForm()}
        return render(request, 'launchpad/activity/activity_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ActivityCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('activities-list')

        return render(request, 'launchpad/activity//activity_create.html', context)
  

### Aircraft Views
    
class AircraftList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_list.html'
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        queryset = Aircraft.objects.all()
        return Response({'aircrafts': queryset})
    
class AircraftDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_detail.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        
        try:
            aircraft_extended = ad.objects.get(aircraft=aircraft_id)            
        except ObjectDoesNotExist as oe: 
            aircraft_extended = 0

        serializer = AircraftFullSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft,'aircraft_extended':aircraft_extended})


class AircraftUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_update.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftFullSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft})

    def post(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftFullSerializer(aircraft, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft': aircraft,'errors':serializer.errors})
        serializer.save()
        return redirect('aircrafts-list')

class AircraftCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftCreateForm()}
        return render(request, 'launchpad/aircraft/aircraft_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AircraftCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('aircrafts-list')

        return render(request, 'launchpad/aircraft/aircraft_create.html', context)
  
    

### Aircraft Extended Views
    
class AircraftExtendedList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_extended/aircraft_extended_list.html'

    def get(self, request):
        queryset = ad.objects.all()
        return Response({'aircraft_extended': queryset})
    
class AircraftExtendedDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_extended/aircraft_extended_detail.html'

    def get(self, request, aircraft_detail_id):
        aircraft_detail = get_object_or_404(ad, pk=aircraft_detail_id)
        
        serializer = AircraftDetailSerializer(aircraft_detail)
        return Response({'serializer': serializer, 'aircraft_extended': aircraft_detail})

class AircraftExtendedUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_extended/aircraft_extended_update.html'

    def get(self, request, aircraft_detail_id):
        aircraft_detail = get_object_or_404(ad, pk=aircraft_detail_id)
        serializer = AircraftDetailSerializer(aircraft_detail)
        return Response({'serializer': serializer, 'aircraft_extended': aircraft_detail})

    def post(self, request, aircraft_detail_id):
        aircraft_detail = get_object_or_404(ad, pk=aircraft_detail_id)
        serializer = AircraftDetailSerializer(aircraft_detail, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft_extended': aircraft_detail,'errors':serializer.errors})
        serializer.save()
        return redirect('aircraft-extended-list')

class AircraftExtendedCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftDetailCreateForm()}
        return render(request, 'launchpad/aircraft_extended/aircraft_extended_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AircraftDetailCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('aircraft-extended-list')

        return render(request, 'launchpad/aircraft_extended/aircraft_extended_create.html', context)
  
    

### Manufacturer Views
    
class ManufacturersList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/manufacturer/manufacturer_list.html'

    def get(self, request):
        queryset = Manufacturer.objects.all()
        return Response({'manufacturers': queryset})
    
class ManufacturersDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/manufacturer/manufacturer_detail.html'

    def get(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        serializer = ManufacturerSerializer(manufacturer)
        return Response({'serializer': serializer, 'manufacturer': manufacturer})


class ManufacturersUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/manufacturer/manufacturer_update.html'

    def get(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        serializer = ManufacturerSerializer(manufacturer)
        return Response({'serializer': serializer, 'manufacturer': manufacturer})

    def post(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        serializer = ManufacturerSerializer(manufacturer, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'manufacturer': manufacturer,'errors':serializer.errors})
        serializer.save()
        return redirect('manufacturers-list')

class ManufacturerCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ManufacturerCreateForm()}
        return render(request, 'launchpad/manufacturer/manufacturer_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ManufacturerCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            
            return redirect('manufacturers-list')
    
        return render(request, 'launchpad/manufacturer/manufacturer_create.html', context)
    
### Firmware Views
    
class FirmwaresList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/firmware/firmware_list.html'

    def get(self, request):
        queryset = Firmware.objects.all()
        return Response({'firmwares': queryset})
    
class FirmwaresDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/firmware/firmware_detail.html'

    def get(self, request, firmware_id):
        firmware = get_object_or_404(Firmware, pk=firmware_id)
        serializer = FirmwareSerializer(firmware)
        return Response({'serializer': serializer, 'firmware': firmware})

    def post(self, request, firmware_id):
        firmware = get_object_or_404(Firmware, pk=firmware_id)
        serializer = FirmwareSerializer(firmware, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'firmware': firmware,'errors':serializer.errors})
        serializer.save()
        return redirect('firmwares-list')

class FirmwareCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': FirmwareCreateForm()}
        return render(request, 'launchpad/firmware/firmware_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FirmwareCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('firmwares-list')

        return render(request, 'launchpad/firmware/firmware_create.html', context)
        
### Flight Plan Views
    
class FlightPlansList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_plan/flightplan_list.html'
    def get(self, request):
        queryset = FlightPlan.objects.all()
        return Response({'flightplans': queryset})
    
class FlightPlansDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_plan/flightplan_detail.html'

    def get(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanSerializer(flightplan)
        return Response({'serializer': serializer, 'flightplan': flightplan})


class FlightPlansUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_plan/flightplan_update.html'
    serializer_class = FlightPlanSerializer
    def get(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanSerializer(flightplan)
        return Response({'serializer': serializer, 'flightplan': flightplan})

    def post(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanSerializer(flightplan, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightplan': flightplan,'errors':serializer.errors})
        serializer.save()
        return redirect('flightplans-list')

class FlightPlanCreateView(CreateView):
    
    model = FlightPlan
    form_class = FlightPlanCreateForm        
    template_name = 'launchpad/flight_plan/flightplan_create.html'    
    
    def post(self, request, *args, **kwargs):
        form = FlightPlanCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('flightplans-list')

        return render(request, 'launchpad/flight_plan/flightplan_create.html', context)
  
     
## Flight Operation Views
    
class FlightOperationsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_list.html'

    def get(self, request):
        queryset = FlightOperation.objects.all()
        return Response({'flightoperations': queryset})
    
class FlightOperationsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_detail.html'

    def get(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        try:
            flightpermission = FlightPermission.objects.get(operation = flightoperation)
        except ObjectDoesNotExist:
            flightpermission = 0 
        serializer = FlightPlanSerializer(flightoperation)
        return Response({'serializer': serializer, 'flightoperation': flightoperation, 'flightpermission':flightpermission})


class FlightOperationsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_update.html'

    def get(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        serializer = FlightOperationSerializer(flightoperation)
        return Response({'serializer': serializer, 'flightoperation': flightoperation})

    def post(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        serializer = FlightOperationSerializer(flightoperation, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightoperation': flightoperation,'errors':serializer.errors})
        serializer.save()
        return redirect('flightoperations-list')

class FlightOperationCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightOperationCreateForm()}
        return render(request, 'launchpad/flight_operation/flightoperation_create.html', context)
    
    def post(self, request, *args, **kwargs):
        form = FlightOperationCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            flight_operation = form.save()
            # Create flight permission
            flight_permission = permissions_issuer.issue_permission(flight_operation_id= flight_operation.id)

            return redirect('flightoperations-list')

        return render(request, 'launchpad/flight_operation/flightoperation_create.html', context)
  
class FlightOperationPermissionCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_permission_thanks.html'

    def get(self, request, flightoperation_id):
        
        flight_operation = get_object_or_404(FlightOperation,pk = flightoperation_id)
        flight_permission = FlightPermission.objects.filter(operation = flight_operation).exists()
        if flight_permission:
            flight_permission = FlightPermission.objects.get(operation = flight_operation)
        else:
            flight_permission = permissions_issuer.issue_permission(flight_operation_id = flight_operation.id)
            flight_permission = flight_permission['permission']
        
        return Response({'flightpermissions': flight_permission})
    
        
### Flight Permission Views
    
class FlightPermissionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission/flightpermission_list.html'

    def get(self, request):
        queryset = FlightPermission.objects.all()
        return Response({'flightpermissions': queryset})
    
class FlightPermissionsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission/flightpermission_detail.html'

    def get(self, request, flightpermission_id):
        flightpermission = get_object_or_404(FlightPermission, pk=flightpermission_id)
        serializer = FlightPermissionSerializer(flightpermission)
        return Response({'serializer': serializer, 'flightpermission': flightpermission})

# class FlightPermissionCreateView(CreateView):
#     def get(self, request, *args, **kwargs):
#         context = {'form': FlightPermissionCreateForm()}
#         return render(request, 'launchpad/flightpermission_create.html', context)

#     def post(self, request, *args, **kwargs):
#         form = FlightPermissionCreateForm(request.POST)
#         context = {'form': form}
#         if form.is_valid():
#             flight_permission = form.save()
#             ## Issue a permission artefact
#             print(flight_permission.operation.flight_plan.id) 
#             return redirect('flightpermissions-list')

#         return render(request, 'launchpad/flightpermission_create.html', context)
  
    
### Flight Permission Artefact Details Views
    
    
class FlightPermissionDigitalSkyList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_digitalsky_list.html'
    
    def get(self, request):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = FlightPermission.objects.filter(is_successful=False)
        return Response({'flightpermissions': queryset})


class FlightPermissionDigitalSkyRequest(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission_digital_sky/flightpermission_digitalsky_detail.html'
    

    def get(self, request, flightpermission_id):
        flightpermission = get_object_or_404(FlightPermission, pk=flightpermission_id)
        serializer = FlightPermissionSerializer(flightpermission)
        return Response({'serializer': serializer, 'flightpermission': flightpermission})

    def post(self, request,flightpermission_id):
        
        # Submit a call to Digital Sky API

        return redirect('flightpermissions-digitalsky-thanks')
    
class FlightPermissionDigitalSkyThanks(TemplateView):
    
    template_name = 'launchpad/flight_permission_digital_sky/flightpermission_digitalsky_thanks.html'

    
class FlightPermissionsArtefactList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission_digital_sky/flightpermission_list.html'

    def get(self, request):
        queryset = FlightPermission.objects.filter(is_successful=True)
        return Response({'flightpermissions': queryset})
    
class FlightPermissionsArtefactDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission_digital_sky/flightpermission_detail.html'

    def get(self, request, flightpermission_id):
        flightpermission = get_object_or_404(FlightPermission, pk=flightpermission_id)
        serializer = FlightPermissionSerializer(flightpermission)
        return Response({'serializer': serializer, 'flightpermission': flightpermission})



### Flight Logs Views
    
class FlightLogsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_log/flightlog_list.html'

    def get(self, request):
        queryset = FlightLog.objects.all()
        return Response({'flightlogs': queryset})
    
class FlightLogsSign(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_log/flightlog_sign_thanks.html'

    def get(self, request, flightlog_id):
        sign_result = log_signer.sign_log(flightlog_id)
        return Response(sign_result)
    

class FlightLogsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_log/flightlog_detail.html'

    def get(self, request, flightlog_id):
        flightlog = get_object_or_404(FlightLog, pk=flightlog_id)
        serializer = FlightLogSerializer(flightlog)
        return Response({'serializer': serializer, 'flightlog': flightlog})

        
class FlightLogsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_log/flightlog_update.html'

    def get(self, request, flightlog_id):
        
        flightlog = get_object_or_404(FlightLog, pk=flightlog_id)
        serializer = FlightLogSerializer(flightlog)
        return Response({'serializer': serializer, 'flightlog': flightlog})

    def post(self, request, flightlog_id):
        
        flightlog = get_object_or_404(FlightLog, pk=flightlog_id)

        serializer = FlightLogSerializer(flightlog, data=request.data)
        
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightlog': flightlog,'errors':serializer.errors})
        serializer.save()
        return redirect('flightlogs-list')


class FlightLogCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightLogCreateForm()}
        return render(request, 'launchpad/flight_log/flightlog_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightLogCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('flightlogs-list')

        return render(request, 'launchpad/flight_log/flightlog_create.html', context)
  
    
    
# class FlightLogsDigitalSkyList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/flight_log_digital_sky/flightlog_digitalsky_list.html'

#     def get(self, request):
#         queryset = FlightLog.objects.filter(is_submitted=False, is_editable=False)
#         return Response({'flightlogs': queryset})
    
# class FlightLogsDigitalSkyDetail(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/flight_log_digital_sky/flightlog_digitalsky_detail.html'

#     def get(self, request, flightlog_id):
#         flightlog = get_object_or_404(FlightLog, pk=flightlog_id)
#         serializer = FlightLogSerializer(flightlog)
#         return Response({'serializer': serializer, 'flightlog': flightlog})


# class FlightLogSubmitDigitalSkyRequest(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/flight_log_digital_sky/flightlog_digitalsky_detail.html'

#     def get(self, request, flightlog_id):
#         flightlog = get_object_or_404(FlightLog, pk=flightlog_id)
#         serializer = FlightLogSerializer(flightlog)
#         return Response({'serializer': serializer, 'flightlog': flightlog})

#     def post(self, request,flightlog_id):        
#         # Submit a call to Digital Sky API

#         return redirect('flightlogs-digitalsky-thanks')
    
       
# class FlightLogDigitalSkyThanks(TemplateView):    
#     template_name = 'launchpad/flight_log_digital_sky/flightlog_digitalsky_thanks.html'
        
### Signed FLight Log Views

    
class SignedFlightLogsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/signed_flight_log/signed_flightlog_list.html'

    def get(self, request):
        queryset = SignedFlightLog.objects.all()
        return Response({'signed_flightlogs': queryset})
    
class SignedFlightLogsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/signed_flight_log/signed_flightlog_detail.html'

    def get(self, request, signed_flightlog_id):
        signed_flightlog = get_object_or_404(SignedFlightLog, pk=signed_flightlog_id)
        serializer = SignedFlightLogSerializer(signed_flightlog_id)
        return Response({'serializer': serializer, 'signed_flightlog': signed_flightlog})
        
### DigitalSky Log Views
    
# class DigitalSkyLogsList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/digital_sky_log/digitalskylog_list.html'

#     def get(self, request):
#         queryset = DigitalSkyLog.objects.all()
#         return Response({'digitalskylogs': queryset})
    
# class DigitalSkyLogsDetail(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/digital_sky_log/digitalskylog_detail.html'

#     def get(self, request, digitalskylog_id):
#         digitalskylog = get_object_or_404(DigitalSkyLog, pk=digitalskylog_id)
#         serializer = DigitalSkyLogSerializer(digitalskylog)
#         return Response({'serializer': serializer, 'digitalskylog': digitalskylog})


# class DigitalSkyLogCreateView(CreateView):
#     def get(self, request, *args, **kwargs):
#         context = {'form': DigitalSkyLogCreateForm()}
#         return render(request, 'launchpad/digital_sky_log/digitalskylog_create.html', context)

#     def post(self, request, *args, **kwargs):
#         form = DigitalSkyLogCreateForm(request.POST)
#         context = {'form': form}
#         if form.is_valid():
#             form.save()
#             return redirect('digitalskylogs-list')

#         return render(request, 'launchpad/digital_sky_log/digitalskylog_create.html', context)
  
 # Digital Sky Transactionss   
    
# class DigitalSkyTransactionsList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/digital_sky_transaction/digitalskytransaction_list.html'

#     def get(self, request):
#         queryset = Transaction.objects.all()
#         return Response({'digitalskytransactions': queryset})
    
# class DigitalSkyTransactionDetail(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'launchpad/digital_sky_transaction/digitalskytransaction_detail.html'

#     def get(self, request, transaction_id):
#         digitalskytransaction = get_object_or_404(Transaction, pk=transaction_id)
#         serializer = TransactionSerializer(digitalskytransaction)
#         return Response({'serializer': serializer, 'digitalskytransaction': digitalskytransaction})


# class DigitalSkyTransactionCreateView(CreateView):
#     def get(self, request, *args, **kwargs):
#         context = {'form': DigitalSkyTransactionCreateForm()}
#         return render(request, 'launchpad/digital_sky_transaction/digitalskytransaction_create.html', context)

#     def post(self, request, *args, **kwargs):
#         form = DigitalSkyTransactionCreateForm(request.POST)
#         context = {'form': form}
#         if form.is_valid():
#             form.save()
#             return redirect('digitalskytransactions-list')

#         return render(request, 'launchpad/digital_sky_transaction/digitalskytransaction_create.html', context)
  
    
    
### Engine Views
    
class EnginesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/engine/engine_list.html'

    def get(self, request):
        queryset = Engine.objects.all()
        return Response({'engines': queryset})
    
class EnginesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/engine/engine_detail.html'

    def get(self, request, engine_id):
        engine = get_object_or_404(Engine, pk=engine_id)
        serializer = EngineSerializer(engine)
        return Response({'serializer': serializer, 'engine': engine})

    def post(self, request, engine_id):
        engine = get_object_or_404(Manufacturer, pk=engine_id)
        serializer = EngineSerializer(engine, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'engine': engine,'errors':serializer.errors})
        serializer.save()
        return redirect('engines-list')

class EngineCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': EngineCreateForm()}
        return render(request, 'launchpad/engine/engine_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EngineCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('engines-list')

        return render(request, 'launchpad/engine/engine_create.html', context)
  
# Aerobridge Credentials View
class CredentialsReadFirst(TemplateView):    
    template_name = 'launchpad/credential/credentials_read_first.html'
    
class CredentialsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential/credential_list.html'
    serializers = AerobridgeCredentialGetSerializer
    def get(self, request):
        queryset = AerobridgeCredential.objects.all()
        return Response({'credentials': queryset})
    
class CredentialsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential/credential_detail.html'

    def get(self, request, credential_id):
        credential = get_object_or_404(AerobridgeCredential, pk=credential_id)
        serializer = AerobridgeCredentialSerializer(credential)
        return Response({'serializer': serializer, 'credential': credential})



class CredentialsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential/credential_update.html'

    def get(self, request, credential_id):
        credential = get_object_or_404(AerobridgeCredential, pk=credential_id)
        serializer = AerobridgeCredentialSerializer(credential)
        
        return Response({'serializer': serializer, 'credential': credential})

    def post(self, request, credential_id):
        credential = get_object_or_404(AerobridgeCredential, pk=credential_id)
        serializer = AerobridgeCredentialSerializer(credential, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'credential': credential,'errors':serializer.errors})
        serializer.save()
        return redirect('credentials-list')

class CredentialsDelete(DestroyAPIView):  
    serializer_class = AerobridgeCredentialSerializer
    def get_credential(self, pk):
        try:
            return AerobridgeCredential.objects.get(pk=pk)
        except AerobridgeCredential.DoesNotExist:
            raise Http404

    def delete(self, request, credential_id, format=None):
        credential = self.get_credential(credential_id)
        credential.delete()
        
        return redirect('credentials-list')


class CredentialsCreateView(CreateView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential/credentials_create.html'
    form_class = TokenCreateForm
    model = AerobridgeCredential

    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')

        f = encrpytion_util.EncrpytionHelper(secret_key= secret_key)

        enc_token = f.encrypt(message = form.data['credential'].encode('utf-8'))
        self.object.token = enc_token
        self.object.save()

    
        return redirect('credentials-list')


# Cloud Files View
    
class CloudFilesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/cloud_file/cloudfiles_list.html'
    serializers = CloudFileSerializer
    def get(self, request):
        queryset = CloudFile.objects.all()
        return Response({'cloudfiles': queryset})
    
class CloudFilesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/cloud_file/cloudfiles_detail.html'

    def get(self, request, cloudfile_id):
        cloudfile = get_object_or_404(CloudFile, pk=cloudfile_id)
        serializer = CloudFileSerializer(cloudfile)
        return Response({'serializer': serializer, 'cloudfile': cloudfile})


class CloudFilesCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (MultiPartParser,)
    def get(self, request, *args, **kwargs):
        context = {'form': CustomCloudFileCreateForm()}
        return render(request, 'launchpad/cloud_file/cloudfiles_upload.html', context)

    def post(self, request, *args, **kwargs):
        form = CustomCloudFileCreateForm(request.POST, request.FILES)        
        if form.is_valid():            
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
                
                try:
                    s3 = boto3.client('s3', region_name =env.get('S3_REGION_NAME','0'), endpoint_url= endpoint_url, aws_access_key_id=env.get('S3_ACCESS_KEY','0'),aws_secret_access_key=env.get('S3_SECRET_KEY','0'))                               
                    
                    s3.upload_fileobj(f, BUCKET_NAME, os.path.join(file_type, file_name))
                except NoCredentialsError as ne:                                        
                    context = {'errors':'File not uploaded, problem  with Cloud Bucket credentials'}   
                    return render(request, 'launchpad/cloud_file/cloudfiles_error.html', context)
                except Exception as e:                     
                    context = {'errors':'File not uploaded, problem with Cloud Bucket configuration, it is improperly configured or not supported, please contact your administrator.'}   
                    return render(request, 'launchpad/cloud_file/cloudfiles_error.html', context)
                else:
                    location = endpoint_url + '/' + file_type + file_name
                    cf = CloudFile(location= location,upload_type = file_type,  name = friendly_name)
                    cf.save()            
                    return redirect('cloud-files-list')
            
        else:            
            context = {'form': CustomCloudFileCreateForm(request.POST, request.FILES), 'errors':form.errors}        
            return render(request, 'launchpad/cloud_file/cloudfiles_upload.html', context)
            