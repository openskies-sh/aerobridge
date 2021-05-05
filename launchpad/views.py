from pki_framework.models import DigitalSkyCredentials
from django.shortcuts import render

from registry.models import Person, Address, Operator, Aircraft, Manufacturer, Firmware, Contact, Pilot, Engine, Activity
from gcs_operations.models import FlightOperation, FlightLog, FlightPlan, FlightPermission, Transaction
from pki_framework.models import DigitalSkyCredentials
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic import TemplateView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import PersonSerializer, AddressSerializer, OperatorSerializer, AircraftSerializer, ManufacturerSerializer, FirmwareSerializer, ContactSerializer, PilotSerializer, EngineSerializer, ActivitySerializer
from digitalsky_provider.serializers import DigitalSkyLogSerializer, AircraftRegisterSerializer
from pki_framework.serializers import DigitalSkyCredentialsSerializer, DigitalSkyCredentialsGetSerializer
from pki_framework import encrpytion_util
from digitalsky_provider.models import DigitalSkyLog, AircraftRegister
from rest_framework.generics import DestroyAPIView
from .forms import PersonCreateForm, AddressCreateForm, OperatorCreateForm , AircraftCreateForm, ManufacturerCreateForm, FirmwareCreateForm, FlightLogCreateForm, FlightOperationCreateForm, FlightPermissionCreateForm, FlightPlanCreateForm, DigitalSkyLogCreateForm, ContactCreateForm, PilotCreateForm,AircraftRosterCreateForm, EngineCreateForm, ActivityCreateForm, CutsomTokenCreateForm
from django.shortcuts import redirect
from django.http import Http404
from rest_framework import status
from django.conf import settings
from gcs_operations.serializers import FlightPlanSerializer, FlightOperationSerializer, FlightPermissionSerializer, TransactionSerializer, FlightLogSerializer

class HomeView(TemplateView):
    template_name = 'launchpad/basecamp.html'

class DigitalSkyReadFirst(TemplateView):
    template_name = 'launchpad/digitalsky_read_first.html'
    
class FlightPermissionsReadFirst(TemplateView):
    template_name = 'launchpad/flight_permissions_read_first.html'

### Person Views 
class PeopleList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/people_list.html'

    def get(self, request):
        queryset = Person.objects.all()
        return Response({'people': queryset})
    
class PersonDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/person_detail.html'

    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        serializer = PersonSerializer(person)
        return Response({'serializer': serializer, 'person': person})

    def post(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        serializer = PersonSerializer(person, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'person': person})
        serializer.save()
        return redirect('people-list')

class PersonCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': PersonCreateForm()}
        return render(request, 'launchpad/person_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PersonCreateForm(request.POST)
        if form.is_valid():
            person = form.save()
            person.save()
            
        return redirect('people-list')
    
    
### Address Views
    
    
class AddressList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/address_list.html'

    def get(self, request):
        queryset = Address.objects.all()
        return Response({'addresses': queryset})
    
class AddressDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/address_detail.html'

    def get(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address)
        return Response({'serializer': serializer, 'address': address})

    def post(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'address': address})
        serializer.save()
        return redirect('addresses-list')

class AddressCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AddressCreateForm()}
        return render(request, 'launchpad/address_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AddressCreateForm(request.POST)
        if form.is_valid():
            address = form.save()
            address.save()
            
        return redirect('addresses-list')


### Address Views
    
    
class OperatorList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/operator_list.html'

    def get(self, request):
        queryset = Operator.objects.all()
        return Response({'operators': queryset})
    
class OperatorDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/operator_detail.html'

    def get(self, request, operator_id):
        operator = get_object_or_404(Operator, pk=operator_id)
        serializer = OperatorSerializer(operator)
        return Response({'serializer': serializer, 'operator': operator})

    def post(self, request, operator_id):
        operator = get_object_or_404(Operator, pk=operator_id)
        serializer = OperatorSerializer(operator, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'operator': operator})
        serializer.save()
        return redirect('operators-list')

class OperatorCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': OperatorCreateForm()}
        return render(request, 'launchpad/operator_create.html', context)

    def post(self, request, *args, **kwargs):
        form = OperatorCreateForm(request.POST)
        if form.is_valid():
            operator = form.save()
            operator.save()
            
        return redirect('operators-list')
    

### Contact Views
    
class ContactsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/contact_list.html'

    def get(self, request):
        queryset = Contact.objects.all()
        return Response({'contacts': queryset})
    
class ContactsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/contact_detail.html'

    def get(self, request, contact_id):
        contact = get_object_or_404(Contact, pk=contact_id)
        serializer = ContactSerializer(contact)
        return Response({'serializer': serializer, 'contact': contact})


class ContactsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ContactCreateForm()}
        return render(request, 'launchpad/contact_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactCreateForm(request.POST)
        if form.is_valid():
            contact = form.save()
            contact.save()
            
        return redirect('contacts-list')
    

### Flight Pilot Views
    
class PilotsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/pilot_list.html'

    def get(self, request):
        queryset = Pilot.objects.all()
        return Response({'pilots': queryset})
    
class PilotsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/pilot_detail.html'

    def get(self, request, pilot_id):
        pilot = get_object_or_404(Pilot, pk=pilot_id)
        serializer = PilotSerializer(Pilot)
        return Response({'serializer': serializer, 'pilot': pilot})


class PilotsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': PilotCreateForm()}
        return render(request, 'launchpad/pilot_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PilotCreateForm(request.POST)
        if form.is_valid():
            pilot = form.save()
            pilot.save()
            
        return redirect('pilots-list')
    


### Activites Views
    
class ActivitiesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/activity_list.html'

    def get(self, request):
        queryset = Activity.objects.all()
        return Response({'activities': queryset})
    
class ActivitiesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/activity_detail.html'

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity)
        return Response({'serializer': serializer, 'activity': activity})


class ActivitiesCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ActivityCreateForm()}
        return render(request, 'launchpad/activity_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ActivityCreateForm(request.POST)
        if form.is_valid():
            activity = form.save()
            activity.save()
            
        return redirect('activities-list')
    

### Aircraft Views
    
class AircraftList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_list.html'

    def get(self, request):
        queryset = Aircraft.objects.all()
        return Response({'aircrafts': queryset})
    
class AircraftDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_detail.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft})



class AircraftUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_update.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft})

    def post(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftSerializer(aircraft, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft': aircraft})
        serializer.save()
        return redirect('aircrafts-list')


class AircraftCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftCreateForm()}
        return render(request, 'launchpad/aircraft_create.html', context)

    def post(self, request, *args, **kwargs):
        form = OperatorCreateForm(request.POST)
        if form.is_valid():
            aircraft = form.save()
            aircraft.save()
            
        return redirect('aircrafts-list')
    
    

### Manufacturer Views
    
class ManufacturersList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/manufacturer_list.html'

    def get(self, request):
        queryset = Manufacturer.objects.all()
        return Response({'manufacturers': queryset})
    
class ManufacturersDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/manufacturer_detail.html'

    def get(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        serializer = ManufacturerSerializer(manufacturer)
        return Response({'serializer': serializer, 'manufacturer': manufacturer})

    def post(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        serializer = ManufacturerSerializer(manufacturer, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'manufacturer': manufacturer})
        serializer.save()
        return redirect('manufacturers-list')

class ManufacturerCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': ManufacturerCreateForm()}
        return render(request, 'launchpad/manufacturer_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ManufacturerCreateForm(request.POST)
        if form.is_valid():
            manufacturer = form.save()
            manufacturer.save()
            
        return redirect('manufacturers-list')
    
    
### Manufacturer Views
    
class FirmwaresList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/firmware_list.html'

    def get(self, request):
        queryset = Firmware.objects.all()
        return Response({'firmwares': queryset})
    
class FirmwaresDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/firmware_detail.html'

    def get(self, request, firmware_id):
        firmware = get_object_or_404(Firmware, pk=firmware_id)
        serializer = FirmwareSerializer(firmware)
        return Response({'serializer': serializer, 'firmware': firmware})

    def post(self, request, firmware_id):
        firmware = get_object_or_404(Firmware, pk=firmware_id)
        serializer = FirmwareSerializer(firmware, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'firmware': firmware})
        serializer.save()
        return redirect('firmwares-list')

class FirmwareCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FirmwareCreateForm()}
        return render(request, 'launchpad/firmware_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FirmwareCreateForm(request.POST)
        if form.is_valid():
            firmware = form.save()
            firmware.save()
            
        return redirect('firmwares-list')
    
        
### Flight Plan Views
    
class FlightPlansList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightplan_list.html'

    def get(self, request):
        queryset = FlightPlan.objects.all()
        return Response({'flightplans': queryset})
    
class FlightPlansDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightplan_detail.html'

    def get(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanSerializer(flightplan)
        return Response({'serializer': serializer, 'flightplan': flightplan})

    def post(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanSerializer(flightplan, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightplan': flightplan})
        serializer.save()
        return redirect('flightplans-list')

class FlightPlanCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightPlanCreateForm()}
        return render(request, 'launchpad/flightplan_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightPlanCreateForm(request.POST)
        if form.is_valid():
            flightplan = form.save()
            flightplan.save()
            
        return redirect('flightplans-list')
    
    
        
### Flight Operation Views
    
class FlightOperationsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightoperation_list.html'

    def get(self, request):
        queryset = FlightOperation.objects.all()
        return Response({'flightoperations': queryset})
    
class FlightOperationsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightoperation_detail.html'

    def get(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        serializer = FlightOperationSerializer(flightoperation)
        return Response({'serializer': serializer, 'flightoperation': flightoperation})

    def post(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        serializer = FlightOperationSerializer(flightoperation, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightoperation': flightoperation})
        serializer.save()
        return redirect('flightoperations-list')

class FlightOperationCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightOperationCreateForm()}
        return render(request, 'launchpad/flightoperation_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightOperationCreateForm(request.POST)
        if form.is_valid():
            flightoperation = form.save()
            flightoperation.save()
            
        return redirect('flightoperations-list')
    
    
        
### Flight Permission Views
    
class FlightPermissionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_list.html'

    def get(self, request):
        queryset = FlightPermission.objects.all()
        return Response({'flightpermissions': queryset})
    
class FlightPermissionsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_detail.html'

    def get(self, request, flightpermission_id):
        flightpermission = get_object_or_404(FlightPermission, pk=flightpermission_id)
        serializer = FlightPermissionSerializer(flightpermission)
        return Response({'serializer': serializer, 'flightpermission': flightpermission})


class FlightPermissionCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightPermissionCreateForm()}
        return render(request, 'launchpad/flightpermission_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightPermissionCreateForm(request.POST)
        if form.is_valid():
            flightpermission = form.save()
            flightpermission.save()
            
        return redirect('flightpermissions-list')
    
    
    
### Flight Permission Artefact Details Views
    
class FlightPermissionsArtefactList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_list.html'

    def get(self, request):
        queryset = FlightPermission.objects.filter(is_successful=True)
        return Response({'flightpermissions': queryset})
    
class FlightPermissionsArtefactDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_detail.html'

    def get(self, request, flightpermission_id):
        flightpermission = get_object_or_404(FlightPermission, pk=flightoperation_id)
        serializer = FlightPermissionSerializer(flightpermission)
        return Response({'serializer': serializer, 'flightpermission': flightpermission})



### Flight Permission Views
    
class FlightLogsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightlog_list.html'

    def get(self, request):
        queryset = FlightLog.objects.all()
        return Response({'flightlogs': queryset})
    
class FlightLogsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flightpermission_detail.html'

    def get(self, request, flightlog_id):
        flightlog = get_object_or_404(FlightLog, pk=flightoperation_id)
        serializer = FlightLogsSerializer(flightlog)
        return Response({'serializer': serializer, 'flightlog': flightlog})

    def post(self, request, flightlog_id):
        flightlog = get_object_or_404(FlightLog, pk=flightoperation_id)
        serializer = FlightLogsSerializer(flightlog, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'flightlog': flightlog})
        serializer.save()
        return redirect('flightlogs-list')

class FlightLogCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': FlightLogCreateForm()}
        return render(request, 'launchpad/flightlog_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightLogCreateForm(request.POST)
        if form.is_valid():
            flightlog = form.save()
            flightlog.save()
            
        return redirect('flightlogs-list')
    
    
    
    
        
### DigitalSky Log Views
    
class DigitalSkyLogsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/digitalskylog_list.html'

    def get(self, request):
        queryset = DigitalSkyLog.objects.all()
        return Response({'digitalskylogs': queryset})
    
class DigitalSkyLogsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/digitalskylog_detail.html'

    def get(self, request, digitalskylog_id):
        digitalskylog = get_object_or_404(DigitalSkyLog, pk=digitalskylog_id)
        serializer = DigitalSkyLogSerializer(digitalskylog)
        return Response({'serializer': serializer, 'digitalskylog': digitalskylog})


class DigitalSkyLogCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': DigitalSkyLogCreateForm()}
        return render(request, 'launchpad/digitalskylog_create.html', context)

    def post(self, request, *args, **kwargs):
        form = DigitalSkyLogCreateForm(request.POST)
        if form.is_valid():
            digitskylog = form.save()
            digitskylog.save()
            
        return redirect('digitalskylogs-list')
    
 # Digital Sky Transactionss   
    
class DigitalSkyTransactionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/digitalskytransaction_list.html'

    def get(self, request):
        queryset = Transaction.objects.all()
        return Response({'digitalskytransactions': queryset})
    
class DigitalSkyTransactionDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/digitalskytransaction_detail.html'

    def get(self, request, transaction_id):
        digitalskytransaction = get_object_or_404(Transaction, pk=transaction_id)
        serializer = TransactionSerializer(digitalskytransaction)
        return Response({'serializer': serializer, 'digitalskytransaction': digitalskytransaction})


class DigitalSkyTransactionCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': DigitalSkyTransactionCreateForm()}
        return render(request, 'launchpad/digitalskytransaction_create.html', context)

    def post(self, request, *args, **kwargs):
        form = DigitalSkyTransactionCreateForm(request.POST)
        if form.is_valid():
            digitalskytransaction = form.save()
            digitalskytransaction.save()
            
        return redirect('digitalskytransactions-list')
    


### Flight Permission Views
    
class AircraftRosterList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraftroster_list.html'

    def get(self, request):
        queryset = AircraftRegister.objects.all()
        return Response({'aircraftrosters': queryset})
    
class AircraftRosterDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraftroster_detail.html'

            
    def get(self, request, aircraftroster_id):
        aircraftroster = get_object_or_404(AircraftRegister, pk=aircraftroster_id)
        serializer = AircraftRegisterSerializer(aircraftroster)
        drone = aircraftroster.drone
        operator = get_object_or_404(Operator, aircraft = drone)
        txn, created = Transaction.objects.get_or_create(aircraft = drone, prefix='registration')
        txn_details = txn.get_txn_id()
        

        return Response({'serializer': serializer, 'aircraftroster': aircraftroster,'operator':operator, 'txn_details':txn_details})

    def post(self, request, aircraftroster_id):
        aircraftroster = get_object_or_404(AircraftRegister, pk=aircraftroster_id)
        serializer = AircraftRegisterSerializer(aircraftroster, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraftroster': aircraftroster})
        serializer.save()
        return redirect('aircraftrosters-list')

class AircraftRosterCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftRosterCreateForm()}
        return render(request, 'launchpad/aircraftroster_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AircraftRosterCreateForm(request.POST)
        if form.is_valid():
            aircraftroster = form.save()
            aircraftroster.save()
            
        return redirect('aircraftrosters-list')
    
    
    
### Manufacturer Views
    
class EnginesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/engine_list.html'

    def get(self, request):
        queryset = Engine.objects.all()
        return Response({'engines': queryset})
    
class EnginesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/engine_detail.html'

    def get(self, request, engine_id):
        engine = get_object_or_404(Engine, pk=engine_id)
        serializer = EngineSerializer(engine)
        return Response({'serializer': serializer, 'engine': engine})

    def post(self, request, engine_id):
        engine = get_object_or_404(Manufacturer, pk=engine_id)
        serializer = EngineSerializer(engine, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'engine': engine})
        serializer.save()
        return redirect('engines-list')

class EngineCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': EngineCreateForm()}
        return render(request, 'launchpad/engine_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EngineCreateForm(request.POST)
        if form.is_valid():
            engine = form.save()
            engine.save()
            
        return redirect('engines-list')
    
    
class CredentialsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential_list.html'
    serializers = DigitalSkyCredentialsGetSerializer
    def get(self, request):
        queryset = DigitalSkyCredentials.objects.all()
        return Response({'credentials': queryset})
    
class CredentialsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential_detail.html'

    def get(self, request, credential_id):
        credential = get_object_or_404(DigitalSkyCredentials, pk=credential_id)
        serializer = DigitalSkyCredentialsGetSerializer(credential)
        return Response({'serializer': serializer, 'credential': credential})

    def post(self, request, credential_id):
        credential = get_object_or_404(DigitalSkyCredentials, pk=credential_id)
        serializer = DigitalSkyCredentialsGetSerializer(credential, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'credential': credential})
        serializer.save()
        return redirect('credentials-list')

class CredentialsDelete(DestroyAPIView):  
    
    def get_credential(self, pk):
        try:
            return DigitalSkyCredentials.objects.get(pk=pk)
        except DigitalSkyCredentials.DoesNotExist:
            raise Http404

    def delete(self, request, credential_id, format=None):
        credential = self.get_credential(credential_id)
        credential.delete()
        
        return redirect('credentials-list')

    

class CredentialsCreateView(CreateView):
    
    def get(self, request, *args, **kwargs):
        context = {'form': CutsomTokenCreateForm()}
        return render(request, 'launchpad/credentials_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CutsomTokenCreateForm(request.POST)

        if form.is_valid():
            serializer = DigitalSkyCredentialsSerializer(data=form.data)
            if serializer.is_valid():
                secret_key = settings.CRYPTOGRAPHY_SALT.encode('utf-8')
                
                f = encrpytion_util.EncrpytionHelper(secret_key= secret_key)
                print(form.data.keys())
                enc_token = f.encrypt(message = form.data['token'].encode('utf-8'))
                
                serializer.save(name = form.data['name'],token=enc_token, environment = form.data['environment'],token_type = form.data['token_type'] )

            
        return redirect('credentials-list')
    

