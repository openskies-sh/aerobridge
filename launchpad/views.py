
from pki_framework.models import AerobridgeCredential
from django.shortcuts import render

from registry.models import AircraftMasterComponent, AircraftModel, Authorization, Person, Address, Operator, Aircraft, Company, Firmware, Contact, Pilot, Activity
from supply_chain_operations.models import Incident
from supply_chain_operations.serializers import IncidentSerializer
from registry.models import AircraftDetail as ad
from registry.models import AircraftComponent , AircraftAssembly
from registry.serializers import AircraftFullSerializer
from gcs_operations.models import CloudFile, FlightOperation, FlightLog, FlightPlan, FlightPermission, SignedFlightLog
from gcs_operations.serializers import CloudFileSerializer, FlightLogSerializer, SignedFlightLogSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic import TemplateView, CreateView, ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import AircraftAssemblySerializer, PersonSerializer, AddressSerializer, OperatorSerializer, AircraftSerializer, CompanySerializer, FirmwareSerializer, ContactSerializer, PilotSerializer, ActivitySerializer, AuthorizationSerializer, AircraftDetailSerializer,FlightPlanReadSerializer, AircraftComponentSerializer, AircraftModelSerializer, AircraftMasterComponentSerializer,AircraftComponentUpdateSerializer, AircraftUpdateSerializer
from pki_framework.serializers import AerobridgeCredentialSerializer, AerobridgeCredentialGetSerializer
# from pki_framework.forms import TokenCreateForm
from pki_framework import encrpytion_util
from jetway.pagination import StandardResultsSetPagination
from rest_framework.generics import DestroyAPIView
from .forms import PersonCreateForm, AddressCreateForm, OperatorCreateForm , AircraftCreateForm, CompanyCreateForm, FirmwareCreateForm, FlightLogCreateForm, FlightOperationCreateForm, AircraftDetailCreateForm, FlightPlanCreateForm,  ContactCreateForm, PilotCreateForm, ActivityCreateForm,CustomCloudFileCreateForm, AuthorizationCreateForm, TokenCreateForm, AircraftComponentCreateForm,AircraftModelCreateForm, AircraftMasterComponentCreateForm, AircraftAssemblyCreateForm, IncidentCreateForm, AircraftAssemblyUpdateForm
from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
from gcs_operations.serializers import FlightPlanSerializer, FlightOperationSerializer, FlightPermissionSerializer, FlightLogSerializer
from supply_chain_operations.serializers import IncidentUpdateSerializer
import tempfile
import arrow
from django.db.models import Exists, OuterRef
from rest_framework.parsers import MultiPartParser
import boto3
from gcs_operations import data_signer, permissions_issuer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from botocore.exceptions import NoCredentialsError
from os import environ as env
from dotenv import load_dotenv, find_dotenv

from django.views import generic
from gcs_operations.utils import Calendar
from supply_chain_operations.utils import IncidentCalendar
from datetime import datetime,timedelta, date
from django.utils.safestring import mark_safe
import calendar

import os


load_dotenv(find_dotenv())

class HomeView(TemplateView):
    template_name = 'launchpad/basecamp.html'

class DigitalSkyReadFirst(TemplateView):
    template_name = 'launchpad/digital_sky/digitalsky_read_first.html'
    
class FlightPermissionsReadFirst(TemplateView):
    template_name = 'launchpad/flight_permission/flight_permissions_read_first.html'
    
class ManufacturingReadFirst(TemplateView):
    template_name = 'launchpad/company/manufacturing_read_first.html'

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
    template_name = 'launchpad/activity/activity_update.html'

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

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft(self):
        try:
            return Aircraft.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_aircraft()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AircraftSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftSerializer(queryset, many=True)
            data = serializer.data        

        
        payload = {'aircrafts': data}
        
        return Response(payload)

class AircraftDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_detail.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        
        try:
            aircraft_extended = ad.objects.get(aircraft=aircraft_id)            
        except ObjectDoesNotExist as oe: 
            aircraft_extended = 0

        try:
            aircraft_assembly = AircraftAssembly.objects.get(aircraft=aircraft_id)            
        except ObjectDoesNotExist as oe: 
            aircraft_assembly = 0
        serializer = AircraftFullSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft,'aircraft_extended':aircraft_extended, 'aircraft_assembly':aircraft_assembly})


class AircraftComponents(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_components.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftFullSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft})



class AircraftUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft/aircraft_update.html'

    def get(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftUpdateSerializer(aircraft)
        return Response({'serializer': serializer, 'aircraft': aircraft})

    def post(self, request, aircraft_id):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        serializer = AircraftUpdateSerializer(aircraft, data=request.data)
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
  


### Aircraft Assemblies Views
    
class AircraftAssembliesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_assembly/aircraft_assembly_list.html'

    pagination_class = StandardResultsSetPagination

    def get_aircraft_assemblies(self, view_type=None):
        view_type_lookup = {'completed':2,'in-progress':0, 'parts-needed':1}
        if view_type is not None: 
            status = view_type_lookup[view_type]
            
            return AircraftAssembly.objects.filter(status = status).order_by('-created_at')            
        else:
            try:
                return AircraftAssembly.objects.all().order_by('-created_at')            
            except Exception as e:
                raise Http404

    def get(self, request, view_type=None):          
        view_type = None if view_type not in ['completed', 'in-progress', 'parts-needed'] else view_type
        queryset = self.get_aircraft_assemblies(view_type=view_type)        
        return Response({'aircraft_assemblies': queryset})
               
        
class AircraftAssembliesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_assembly/aircraft_assembly_detail.html'

    def get(self, request, aircraft_assembly_id):
        aircraft_assembly = get_object_or_404(AircraftAssembly, pk=aircraft_assembly_id)
        
        assembly_components = aircraft_assembly.components.all().order_by('-status')
        
        serializer = AircraftAssemblySerializer(aircraft_assembly)
        return Response({'serializer': serializer, 'aircraft_assembly': aircraft_assembly,'assembly_components':assembly_components})

class AircraftAssembliesUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_assembly/aircraft_assembly_update.html'

    def get(self, request, aircraft_assembly_id):
        aircraft_assembly = get_object_or_404(AircraftAssembly, pk=aircraft_assembly_id)
        serializer = AircraftAssemblySerializer(aircraft_assembly)
        return Response({'serializer': serializer, 'aircraft_assembly': aircraft_assembly})

    def post(self, request, aircraft_assembly_id):
        aircraft_assembly = get_object_or_404(AircraftAssembly, pk=aircraft_assembly_id)
        serializer = AircraftAssemblySerializer(aircraft_assembly, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft_assembly': aircraft_assembly,'errors':serializer.errors})
        serializer.save()
        return redirect('aircraft-assemblies-list')

class AircraftAssembliesComponentsUpdate(APIView):
    
    def get(self, request, aircraft_assembly_id):
        aircraft_assembly_exists = AircraftAssembly.objects.filter(id = aircraft_assembly_id).exists()
        if not aircraft_assembly_exists: 
            raise Http404
        else: 
            aircraft_assembly = AircraftAssembly.objects.get(id = aircraft_assembly_id)
        # aircraft = Aircraft.objects.get(final_assembly= aircraft_assembly)
        aircraft_model = aircraft_assembly.aircraft_model
        context = {'form': AircraftAssemblyUpdateForm(aircraft_assembly_id=aircraft_assembly_id), 'aircraft_model':aircraft_model,'aircraft_assembly': aircraft_assembly}
        return render(request, 'launchpad/aircraft_assembly/aircraft_assembly_component_update.html', context)

    def post(self, request, aircraft_assembly_id):
        aircraft_assembly_exists = AircraftAssembly.objects.filter(id = aircraft_assembly_id).exists()
        if not aircraft_assembly_exists: 
            raise Http404
        else: 
            aircraft_assembly = AircraftAssembly.objects.get(id = aircraft_assembly_id)
        # aircraft = Aircraft.objects.get(final_assembly= aircraft_assembly)

        form = AircraftAssemblyUpdateForm(request.POST, aircraft_assembly_id= aircraft_assembly_id,  instance = aircraft_assembly)
        if form.is_valid():            
            form.save()
            return redirect('aircraft-assemblies-list')
        
        aircraft_model = aircraft_assembly.aircraft_model
        context = {'form': form,'aircraft_model':aircraft_model,'aircraft_assembly': aircraft_assembly}

        return render(request, 'launchpad/aircraft_assembly/aircraft_assembly_component_update.html', context)


class AircraftAssembliesCreateView(CreateView):
    def get(self, request,aircraft_model_id):

        aircraft_model = AircraftModel.objects.filter(id = aircraft_model_id).exists()

        if not aircraft_model:
            raise Http404
        else: 
            aircraft_model = AircraftModel.objects.get(id = aircraft_model_id)
        
        context = {'form': AircraftAssemblyCreateForm(aircraft_model_id=aircraft_model_id), 'aircraft_model':aircraft_model}
        return render(request, 'launchpad/aircraft_assembly/aircraft_assembly_create.html', context)

    def post(self, request,aircraft_model_id):
        aircraft_model = AircraftModel.objects.filter(id = aircraft_model_id).exists()
        submitted_components_master_components = []

        if not aircraft_model:
            raise Http404
        else: 
            aircraft_model = AircraftModel.objects.get(id = aircraft_model_id)

        form = AircraftAssemblyCreateForm(request.POST, aircraft_model_id=aircraft_model_id)
        if form.is_valid():            
            form.save()
            return redirect('aircraft-assemblies-list')
        
        submitted_components = request.POST.getlist('components',None)
                
        for submitted_component in submitted_components:           
            s_c = AircraftComponent.objects.get(id = submitted_component)
            master_component_id = s_c.supplier_part.manufacturer_part.master_component.id            
            submitted_components_master_components.append(str(master_component_id))


        context = {'form': form,'aircraft_model':aircraft_model,'submitted_components':submitted_components_master_components}

        return render(request, 'launchpad/aircraft_assembly/aircraft_assembly_create.html', context)


### Aircraft Models Views
    
class AircraftModelsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_model/aircraft_models_list.html'

    pagination_class = StandardResultsSetPagination
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft_models(self):
        try:
            return AircraftModel.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_aircraft_models()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AircraftModelSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftModelSerializer(queryset, many=True)
            data = serializer.data        
        
        payload = {'aircraft_models': data}
        
        return Response(payload)

        
class AircraftModelsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_model/aircraft_models_detail.html'

    def get(self, request, aircraft_model_id):
        aircraft_model = get_object_or_404(AircraftModel, pk=aircraft_model_id)
        
        aircraft_master_components = aircraft_model.master_components.all()
        
        serializer = AircraftModelSerializer(aircraft_master_components)
        return Response({'serializer': serializer, 'aircraft_model': aircraft_model,'aircraft_master_components':aircraft_master_components})

class AircraftModelsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_model/aircraft_models_update.html'

    def get(self, request, aircraft_model_id):
        aircraft_model = get_object_or_404(AircraftModel, pk=aircraft_model_id)
        serializer = AircraftModelSerializer(aircraft_model)
        return Response({'serializer': serializer, 'aircraft_model': aircraft_model})

    def post(self, request, aircraft_model_id):
        aircraft_model = get_object_or_404(AircraftModel, pk=aircraft_model_id)
        serializer = AircraftModelSerializer(aircraft_model, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft_model': aircraft_model,'errors':serializer.errors})
        serializer.save()
        return redirect('aircraft-models-list')

class AircraftModelsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftModelCreateForm()}
        return render(request, 'launchpad/aircraft_model/aircraft_models_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AircraftModelCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('aircraft-models-list')

        return render(request, 'launchpad/aircraft_model/aircraft_models_create.html', context)
      

class AircraftModelMasterComponents(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_model/aircraft_model_components.html'

    def get(self, request, aircraft_model_id):
        aircraft_model = get_object_or_404(AircraftModel, pk=aircraft_model_id)
        serializer = AircraftModel(aircraft_model)
        return Response({'serializer': serializer, 'aircraft_model': aircraft_model})

    
### Aircraft Master Component Views
    
class AircraftMasterComponentsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_master_component/aircraft_master_components_list.html'

    pagination_class = StandardResultsSetPagination
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft_components(self):
        try:
            return AircraftMasterComponent.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_aircraft_components()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AircraftMasterComponentSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftMasterComponentSerializer(queryset, many=True)
            data = serializer.data        
        
        payload = {'aircraft_master_components': data}
        
        return Response(payload)

          
    
class AircraftMasterComponentsStockDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_master_component_stock_keeping/aircraft_master_components_stock_keeping.html'

    pagination_class = StandardResultsSetPagination
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft_components(self, aircraft_master_component_id=None):
        if aircraft_master_component_id: 
            try:
                return AircraftMasterComponent.objects.filter(id =aircraft_master_component_id).order_by('-created_at')	            
            except Exception as e:
                raise Http404
        else:
            try:
                return AircraftMasterComponent.objects.all().order_by('-created_at')	            
            except Exception as e:
                raise Http404

    def get(self, request, aircraft_master_component_id=None, *args, **kwargs):        
        
        queryset = self.get_aircraft_components(aircraft_master_component_id= aircraft_master_component_id)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AircraftMasterComponentSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftMasterComponentSerializer(queryset, many=True)
            data = serializer.data        
        
        payload = {'aircraft_master_components': data}
        
        return Response(payload)

          
class AircraftMasterComponentsFamilyList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_master_component/aircraft_master_components_list.html'

    pagination_class = StandardResultsSetPagination
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft_components(self, aircraft_master_component_family):
        
        try:
            return AircraftMasterComponent.objects.filter(family = aircraft_master_component_family).order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self,  request, aircraft_master_component_family):
        
        queryset = self.get_aircraft_components(aircraft_master_component_family =aircraft_master_component_family)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AircraftMasterComponentSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftMasterComponentSerializer(queryset, many=True)
            data = serializer.data        
        
        payload = {'aircraft_master_components': data, 'family_filter':True}
        
        return Response(payload)

        
class AircraftMasterComponentsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_master_component/aircraft_master_components_detail.html'

    def get(self, request, aircraft_master_component_id):
        aircraft_master_component = get_object_or_404(AircraftMasterComponent, pk=aircraft_master_component_id)
        components = AircraftComponent.objects.filter(Q(master_component=aircraft_master_component) | Q(supplier_part__manufacturer_part__master_component =aircraft_master_component))

        serializer = AircraftMasterComponentSerializer(aircraft_master_component_id)
        return Response({'serializer': serializer, 'aircraft_master_component': aircraft_master_component, 'components':components})

class AircraftMasterComponentsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_master_component/aircraft_master_components_update.html'

    def get(self, request, aircraft_master_component_id):
        aircraft_master_component = get_object_or_404(AircraftMasterComponent, pk=aircraft_master_component_id)
        serializer = AircraftMasterComponentSerializer(aircraft_master_component)
        return Response({'serializer': serializer, 'aircraft_master_component': aircraft_master_component})

    def post(self, request, aircraft_master_component_id):
        aircraft_master_component = get_object_or_404(AircraftMasterComponent, pk=aircraft_master_component_id)
        serializer = AircraftMasterComponentSerializer(aircraft_master_component, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft_master_component': aircraft_master_component,'errors':serializer.errors})
        serializer.save()
        return redirect('aircraft-master-components-list')

class AircraftMasterComponentsCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': AircraftMasterComponentCreateForm()}
        return render(request, 'launchpad/aircraft_master_component/aircraft_master_components_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AircraftMasterComponentCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('aircraft-master-components-list')

        return render(request, 'launchpad/aircraft_master_component/aircraft_master_components_create.html', context)
      


### Aircraft Component Views
    
class AircraftComponentsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_list.html'

    pagination_class = StandardResultsSetPagination
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_aircraft_components(self, view_type):

        if view_type:
            
            return AircraftComponent.objects.filter(~Exists(AircraftAssembly.objects.filter(components__in =OuterRef('pk')))).filter(status = view_type)
        else:
            try:
                return AircraftComponent.objects.all().order_by('created_at')	            
            except Exception as e:
                raise Http404

    def get(self, request, view_type=None):          
        
        view_type = None if view_type not in ['available'] else 10
        queryset = self.get_aircraft_components(view_type=view_type)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AircraftComponentSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AircraftComponentSerializer(queryset, many=True)
            data = serializer.data        
        
        payload = {'aircraft_components': data}
        
        return Response(payload)
        
class AircraftComponentsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_detail.html'

    def get(self, request, aircraft_component_id):
        aircraft_component = get_object_or_404(AircraftComponent, pk=aircraft_component_id)
        component_in_assembly = AircraftAssembly.objects.filter(components__in = [aircraft_component]).exists()
        

        serializer = AircraftComponentSerializer(aircraft_component)
        return Response({'serializer': serializer, 'aircraft_component': aircraft_component, 'component_in_assembly':component_in_assembly})

class AircraftComponentsRemove(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_remove.html'

    def get(self, request, aircraft_component_id):
        aircraft_component = get_object_or_404(AircraftComponent, pk=aircraft_component_id)

        relevant_assembiles = AircraftAssembly.objects.filter(components__in = [aircraft_component])
        

        for assembly in relevant_assembiles:
            assembly.components.remove(aircraft_component)
            assembly.status = 1
            
            assembly.save()
            relevant_aircraft = Aircraft.objects.filter(final_assembly = assembly)
        
            for r in relevant_aircraft:
                r.status =0
                r.save()

        serializer = AircraftComponentSerializer(aircraft_component)
        return Response({'serializer': serializer, 'aircraft_component': aircraft_component})

class AircraftComponentsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_update.html'

    def get(self, request, aircraft_component_id):
        aircraft_component = get_object_or_404(AircraftComponent, pk=aircraft_component_id)
        serializer = AircraftComponentUpdateSerializer(aircraft_component)
        return Response({'serializer': serializer, 'aircraft_component': aircraft_component})

    def post(self, request, aircraft_component_id):
        aircraft_component = get_object_or_404(AircraftComponent, pk=aircraft_component_id)
        serializer = AircraftComponentUpdateSerializer(aircraft_component, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'aircraft_component': aircraft_component,'errors':serializer.errors})
        serializer.save()
        return redirect('aircraft-components-list')

class AircraftComponentsCreateView(CreateView):
    form_class = AircraftComponentCreateForm
    template_name = 'launchpad/aircraft_component/aircraft_components_create.html'
    def get_context_data(self, *args, **kwargs):
        aircraft_master_component_id = self.kwargs.get('aircraft_master_component_id')
        master_component = get_object_or_404(AircraftMasterComponent, pk=aircraft_master_component_id)
        context = super(AircraftComponentsCreateView, self).get_context_data(**kwargs)
        context['form'] =AircraftComponentCreateForm(aircraft_master_component_id = aircraft_master_component_id)
        # return render(request, 'launchpad/aircraft_component/aircraft_components_create.html', context)
        return context

    def form_valid(self, form,*args, **kwargs):
        aircraft_master_component_id = self.kwargs.get('aircraft_master_component_id')
        master_component = get_object_or_404(AircraftMasterComponent, pk=aircraft_master_component_id)        
        form.save()
        return redirect('aircraft-components-list-filtered',view_type='available')
        
class AircraftComponentsSearchView(APIView):
    model = AircraftComponent
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_search.html' 

    def get_queryset(self):  # new
        query = self.request.GET.get("q1", None)
        query1 = self.request.GET.get("q2", None)
        query2 = self.request.GET.get("q3", None)
        q_list = [query, query1, query2]
        # raise Exception(q_list)
        if None not in q_list:

            key = '-'.join(q_list)
            # raise Exception(key)
            aircraft_components = AircraftComponent.objects.filter(
            Q(aerobridge_id=key)
            )
        else: 
            aircraft_components = AircraftComponent.objects.none()
        return aircraft_components

    def get(self, request):
        components = self.get_queryset()
        return Response({'aircraft_components': components})
        
class AircraftComponentsHistoryView(APIView):
    model = AircraftComponent
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_history.html' 

    def get(self, request, aerobridge_id):
        component = get_object_or_404(AircraftComponent, aerobridge_id=aerobridge_id)
        all_component_history = component.history.all()
        all_component_history_diff = []
        old_record = None
        for current_component_history in all_component_history:
            if old_record:
                delta = current_component_history.diff_against(old_record)                
                for change in delta.changes:                    
                    all_component_history_diff.append([current_component_history, ("{} changed from {} to {}".format(change.field, change.old, change.new))])
                
            else:
                all_component_history_diff.append([current_component_history, "Initial part creation"])
            old_record = current_component_history
                

        return Response({'aircraft_component_history': all_component_history_diff })
        
        
class AircraftComponentsSearchResultsView(ListView):
    model = AircraftComponent
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/aircraft_component/aircraft_components_search_results.html' 

    def get_queryset(self): # new
        
        query = self.request.GET.get("q")
        
        object_list = AircraftComponent.objects.filter(
            Q(master_component__name__icontains=query) | Q(supplier_part__manufacturer_part__master_component__name__icontains=query)
        )
        
        return object_list
        
### Company Views
    
class CompaniesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/company/company_list.html'

    def get(self, request):
        queryset = Company.objects.all()
        return Response({'companies': queryset})
    
class CompaniesDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/company/company_detail.html'

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        serializer = CompanySerializer(company)
        return Response({'serializer': serializer, 'company': company})


class CompaniesUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/company/company_update.html'

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        serializer = CompanySerializer(company)
        return Response({'serializer': serializer, 'company': company})

    def post(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        serializer = CompanySerializer(company, data=request.data)
        
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'company': company,'errors':serializer.errors})
            
        serializer.save()
        return redirect('companies-list')

class CompanyCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': CompanyCreateForm()}
        return render(request, 'launchpad/company/company_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CompanyCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            
            return redirect('companies-list')
    
        return render(request, 'launchpad/company/company_create.html', context)
    
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

class FirmwaresUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/firmware/firmware_update.html'

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
    pagination_class = StandardResultsSetPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_queryset(self):
        try:
            
            return FlightPlan.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlightPlanSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = FlightPlanSerializer(queryset, many=True)
            data = serializer.data        

        
        payload = {'flightplans': data}
        
        return Response(payload)

class FlightPlansDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_plan/flightplan_detail.html'

    def get(self, request, flightplan_id):
        flightplan = get_object_or_404(FlightPlan, pk=flightplan_id)
        serializer = FlightPlanReadSerializer(flightplan)
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
    
    def get(self, request, *args, **kwargs):
        context = {'form': FlightPlanCreateForm()}
        return render(request, 'launchpad/flight_plan/flightplan_create.html', context)

    def post(self, request, *args, **kwargs):
        form = FlightPlanCreateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('flightplans-list')

        return render(request, 'launchpad/flight_plan/flightplan_create.html', context)
  
     
## Flight Operation Views
    

class FlightOperationsCalendar(generic.ListView):
    model = FlightOperation
    template_name = 'launchpad/flight_operation/flightoperation_calendar.html'

    def get_context_data(self, **kwargs):
        def get_date(req_day):
            if req_day:
                year, month = (int(x) for x in req_day.split('-'))
                return date(year, month, day=1)
            return datetime.today()

        def get_date(req_month):
            if req_month:
                year, month = (int(x) for x in req_month.split('-'))
                return date(year, month, day=1)
            return datetime.today()

        def prev_month(d):
            first = d.replace(day=1)
            prev_month = first - timedelta(days=1)
            month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
            return month

        def next_month(d):
            days_in_month = calendar.monthrange(d.year, d.month)[1]
            last = d.replace(day=days_in_month)
            next_month = last + timedelta(days=1)
            month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
            return month

        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class FlightOperationsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_list.html'
    pagination_class = StandardResultsSetPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_queryset(self):
        try:

            return FlightOperation.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlightOperationSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = FlightOperationSerializer(queryset, many=True)
            data = serializer.data        

        
        payload = {'flightoperations': data}
        
        return Response(payload)

class FlightOperationsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_operation/flightoperation_detail.html'

    def get(self, request, flightoperation_id):
        flightoperation = get_object_or_404(FlightOperation, pk=flightoperation_id)
        try:
            flightpermission = FlightPermission.objects.get(operation = flightoperation)
        except ObjectDoesNotExist:
            flightpermission = 0 
        
        serializer = FlightOperationSerializer(flightoperation)
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
            now = arrow.now()
            start_datetime = flight_operation.start_datetime
            operation_start_time_delta = start_datetime - now         
            
            if not (operation_start_time_delta.total_seconds() < 3600 and operation_start_time_delta.total_seconds() > 60):
                
                return Response({'errors': "Cannot issue permissions for operations whose start time is in the past or more than a hour from now"})
            
            flight_permission = permissions_issuer.issue_permission(flight_operation_id = flight_operation.id)
            flight_permission = flight_permission['flight_permission']
                    
        return Response({'flightpermissions': flight_permission})


### Flight Permission Views
    
class FlightPermissionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/flight_permission/flightpermission_list.html'
    pagination_class = StandardResultsSetPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_queryset(self):
        try:
            
            return FlightPermission.objects.all().order_by('-created_at')	            
        except Exception as e:
            raise Http404

    def get(self, request, *args, **kwargs):        
        
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlightPermissionSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = FlightPermissionSerializer(queryset, many=True)
            data = serializer.data        

        
        payload = {'flightpermissions': data}
        
        return Response(payload)
        
    
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
        sign_result = data_signer.sign_log(flightlog_id)
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
  
    
    
# Aerobridge Credentials View
class CredentialsReadFirst(TemplateView):    
    template_name = 'launchpad/credential/credentials_read_first.html'
    
class CredentialsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/credential/credential_list.html'
    pagination_class = StandardResultsSetPagination
    serializers = AerobridgeCredentialGetSerializer

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


    def get_credentials(self):
        
        return AerobridgeCredential.objects.all().order_by('-created_at')	       
            

    def get(self, request):
        queryset = self.get_credentials()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AerobridgeCredentialGetSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = AerobridgeCredentialGetSerializer(queryset, many=True)
            data = serializer.data        

        
        payload = {'credentials': data}
        
        return Response(payload)
    
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
            

### Incidents




class IncidentsCalendar(generic.ListView):
    model = Incident
    template_name = 'launchpad/incidents/incident_calendar.html'

    def get_context_data(self, **kwargs):
        def get_date(req_day):
            if req_day:
                year, month = (int(x) for x in req_day.split('-'))
                return date(year, month, day=1)
            return datetime.today()

        def get_date(req_month):
            if req_month:
                year, month = (int(x) for x in req_month.split('-'))
                return date(year, month, day=1)
            return datetime.today()

        def prev_month(d):
            first = d.replace(day=1)
            prev_month = first - timedelta(days=1)
            month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
            return month

        def next_month(d):
            days_in_month = calendar.monthrange(d.year, d.month)[1]
            last = d.replace(day=days_in_month)
            next_month = last + timedelta(days=1)
            month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
            return month

        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = IncidentCalendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context



class IncidentsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/incidents/incident_list.html'

    def get(self, request):
        queryset = Incident.objects.all().order_by('-created_at')
        return Response({'incidents': queryset})
    
class IncidentsUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/incidents/incident_update.html'

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, pk=incident_id)
        serializer = IncidentUpdateSerializer(incident)
        return Response({'serializer': serializer, 'incident': incident})

    def post(self, request, incident_id):
        incident = get_object_or_404(Incident, pk=incident_id)
        serializer = IncidentUpdateSerializer(incident, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'incident': incident,'errors':serializer.errors})
        serializer.save()
        return redirect('incidents-list')


class IncidentsDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'launchpad/incidents/incident_detail.html'

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, pk=incident_id)
        serializer = IncidentSerializer(incident)
        return Response({'serializer': serializer, 'incident': incident})


class IncidentsCreateView(CreateView):

    
    def get(self, request, aircraft_id, *args, **kwargs):
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        context = {'form': IncidentCreateForm(aircraft_id=aircraft_id), 'aircraft':aircraft}
        return render(request, 'launchpad/incidents/incident_create.html', context)

    def post(self, request, aircraft_id, *args, **kwargs):
        
        aircraft = get_object_or_404(Aircraft, pk=aircraft_id)
        form = IncidentCreateForm(aircraft_id, request.POST)
        context = {'form': form, 'aircraft':aircraft}
        if form.is_valid():
            form.save()
            # tmp = form.save(commit=False)
            # tmp.aircraft = aircraft  
            # aircraft.status = 0
            # aircraft.save()
            # print(tmp.impacted_components)          
            # tmp.save()
            return redirect('incidents-list')
            
        return render(request, 'launchpad/incidents/incident_create.html', context)
  