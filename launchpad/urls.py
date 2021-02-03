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
 
    path('manufacturers', launchpad_views.ManufacturersList.as_view(), name='manufacturers-list'),
    path('manufacturers/<uuid:manufacturer_id>', launchpad_views.ManufacturersDetail.as_view(), name='manufacturers-detail'),
    path('manufacturers/new', launchpad_views.ManufacturerCreateView.as_view(), name='manufacturers-create'),
    
    path('firmwares', launchpad_views.FirmwaresList.as_view(), name='firmwares-list'),
    path('firmwares/<uuid:manufacturer_id>', launchpad_views.FirmwaresDetail.as_view(), name='firmwares-detail'),
    path('firmwares/new', launchpad_views.FirmwareCreateView.as_view(), name='firmwares-create'),
 
    path('flightplans', launchpad_views.FlightPlansList.as_view(), name='flightplans-list'),
    path('flightplans/<uuid:flightplan_id>', launchpad_views.FlightPlansDetail.as_view(), name='flightplans-detail'),
    path('flightplans/new', launchpad_views.FlightPlanCreateView.as_view(), name='flightplans-create'),
  
    path('flightoperations', launchpad_views.FlightOperationsList.as_view(), name='flightoperations-list'),
    path('flightoperations/<uuid:flightoperation_id>', launchpad_views.FlightOperationsDetail.as_view(), name='flightoperations-detail'),
    path('flightoperations/new', launchpad_views.FlightOperationCreateView.as_view(), name='flightoperations-create'),
 
    path('flightpermissions', launchpad_views.FlightPermissionsList.as_view(), name='flightpermissions-list'),
    path('flightpermissions/<uuid:flightpermission_id>', launchpad_views.FlightPermissionsDetail.as_view(), name='flightpermissions-detail'),
    path('flightpermissions/new', launchpad_views.FlightPermissionCreateView.as_view(), name='flightpermissions-create'),
 
    path('flightpermissionartefacts', launchpad_views.FlightPermissionsList.as_view(), name='flightpermissionartefacts-list'),
    path('flightpermissionartefacts/<uuid:flightpermission_id>', launchpad_views.FlightPermissionsDetail.as_view(), name='flightpermissionartefacts-detail'),
    
    path('flightlogs', launchpad_views.FlightLogsList.as_view(), name='flightlogs-list'),
    path('flightlogs/<uuid:flightpermission_id>', launchpad_views.FlightLogsDetail.as_view(), name='flightlogs-detail'),
    path('flightlogs/new', launchpad_views.FlightLogCreateView.as_view(), name='flightlogs-create'),
 
 
    
]