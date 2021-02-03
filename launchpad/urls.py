from django.urls import path, re_path
from . import views as launchpad_views

urlpatterns = [
     path('', launchpad_views.HomeView.as_view()),
    path('addresses', launchpad_views.AddressList.as_view(), name='addresses-list'),
    path('addresses/<uuid:address_id>', launchpad_views.AddressDetail.as_view(), name='addresses-detail'),
    path('addresses/new', launchpad_views.AddressCreateView.as_view(), name='addresses-create'),

    path('people', launchpad_views.PeopleList.as_view(), name='people-list'),
    path('people/<uuid:person_id>', launchpad_views.PersonDetail.as_view(), name='people-detail'),
    path('people/new', launchpad_views.PersonCreateView.as_view(), name='people-create'),
 
    
    path('operators', launchpad_views.OperatorList.as_view(), name='operators-list'),
    path('operators/<uuid:operator_id>', launchpad_views.OperatorDetail.as_view(), name='operators-detail'),
    path('operators/new', launchpad_views.OperatorCreateView.as_view(), name='operators-create'),
 
    path('aircrafts', launchpad_views.AircraftList.as_view(), name='aircrafts-list'),
    path('aircrafts/<uuid:aircraft_id>', launchpad_views.AircraftDetail.as_view(), name='aircrafts-detail'),
    path('aircrafts/new', launchpad_views.AircraftCreateView.as_view(), name='aircrafts-create'),
 
    
]