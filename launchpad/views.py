from django.shortcuts import render
from registry.models import Person, Address, Operator, Aircraft
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import PersonSerializer, AddressSerializer, OperatorSerializer, AircraftSerializer
from django.views.generic import CreateView
from .forms import PersonCreateForm, AddressCreateForm, OperatorCreateForm , AircraftCreateForm
from django.shortcuts import redirect



class HomeView(TemplateView):
    template_name = 'launchpad/basecamp.html'

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
            address = form.save()
            address.save()
            
        return redirect('operators-list')
    


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
            address = form.save()
            address.save()
            
        return redirect('aircrafts-list')