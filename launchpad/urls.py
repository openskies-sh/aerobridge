from django.urls import path, re_path
from . import views as launchpad_views

urlpatterns = [
    path('', launchpad_views.HomeView.as_view()),
    path('addresses', launchpad_views.AddressList.as_view(), name='addresses-list'),
    path('addresses/<uuid:address_id>', launchpad_views.AddressDetail.as_view(), name='addresses-detail'),
    path('addresses/new', launchpad_views.AddressCreateView.as_view(), name='addresses-create'),

    path('people', launchpad_views.PeopleList.as_view(), name='people-list'),
    path('people/<uuid:person_id>', launchpad_views.PersonUpdate.as_view(), name='people-update'),
    path('people/<uuid:person_id>/detail', launchpad_views.PersonDetail.as_view(), name='people-detail'),
    path('people/new', launchpad_views.PersonCreateView.as_view(), name='people-create'),
 
    path('operators', launchpad_views.OperatorList.as_view(), name='operators-list'),
    path('operators/<uuid:operator_id>', launchpad_views.OperatorUpdate.as_view(), name='operators-update'),
    path('operators/<uuid:operator_id>/detail', launchpad_views.OperatorDetail.as_view(), name='operators-detail'),
    path('operators/new', launchpad_views.OperatorCreateView.as_view(), name='operators-create'),

    path('contacts', launchpad_views.ContactsList.as_view(), name='contacts-list'),
    path('contacts/<uuid:contact_id>', launchpad_views.ContactsUpdate.as_view(), name='contacts-update'),
    path('contacts/<uuid:contact_id>/detail', launchpad_views.ContactsDetail.as_view(), name='contacts-detail'),
    path('contacts/new', launchpad_views.ContactsCreateView.as_view(), name='contacts-create'),
 
    path('pilots', launchpad_views.PilotsList.as_view(), name='pilots-list'),
    path('pilots/<uuid:pilot_id>', launchpad_views.PilotsUpdate.as_view(), name='pilots-update'),
    path('pilots/<uuid:pilot_id>/detail', launchpad_views.PilotsDetail.as_view(), name='pilots-detail'),
    path('pilots/new', launchpad_views.PilotsCreateView.as_view(), name='pilots-create'),
     
    path('activities', launchpad_views.ActivitiesList.as_view(), name='activities-list'),
    path('activities/<uuid:activity_id>', launchpad_views.ActivitiesUpdate.as_view(), name='activities-update'),
    path('activities/<uuid:activity_id>/detail', launchpad_views.ActivitiesDetail.as_view(), name='activities-detail'),
    path('activities/new', launchpad_views.ActivitiesCreateView.as_view(), name='activities-create'),
     
    path('authorizations', launchpad_views.AuthorizationsList.as_view(), name='authorizations-list'),
    path('authorizations/<uuid:authorization_id>', launchpad_views.AuthorizationsUpdate.as_view(), name='authorizations-update'),
    path('authorizations/<uuid:authorization_id>/detail', launchpad_views.AuthorizationsDetail.as_view(), name='authorizations-detail'),
    path('authorizations/new', launchpad_views.AuthorizationsCreateView.as_view(), name='authorizations-create'),
     
    path('aircrafts', launchpad_views.AircraftList.as_view(), name='aircrafts-list'),
    path('aircrafts/<uuid:aircraft_id>', launchpad_views.AircraftUpdate.as_view(), name='aircrafts-update'),
    path('aircrafts/<uuid:aircraft_id>/detail', launchpad_views.AircraftDetail.as_view()), 
    path('aircrafts/<uuid:aircraft_id>/components', launchpad_views.AircraftComponents.as_view(), name='aircrafts-detail'),
    path('aircrafts/new', launchpad_views.AircraftCreateView.as_view(), name='aircrafts-create'),

    path('aircraft-extended', launchpad_views.AircraftExtendedList.as_view(), name='aircraft-extended-list'),
    path('aircraft-extended/<uuid:aircraft_detail_id>', launchpad_views.AircraftExtendedUpdate.as_view(), name='aircraft-extended-update'),
    path('aircraft-extended/<uuid:aircraft_detail_id>/detail', launchpad_views.AircraftExtendedDetail.as_view(), name='aircraft-extended-detail'),
    path('aircraft-extended/new', launchpad_views.AircraftExtendedCreateView.as_view(), name='aircraft-extended-create'),
 
    path('manufacturing-read-first', launchpad_views.ManufacturingReadFirst.as_view(), name='manufacturing-read-first'),
     
    path('aircraft-models', launchpad_views.AircraftModelsList.as_view(), name='aircraft-models-list'),
    path('aircraft-models/<uuid:aircraft_model_id>', launchpad_views.AircraftModelsUpdate.as_view(), name='aircraft-models-update'),
    path('aircraft-models/<uuid:aircraft_model_id>/detail', launchpad_views.AircraftModelsDetail.as_view(), name='aircraft-models-detail'),
    path('aircraft-models/new', launchpad_views.AircraftModelsCreateView.as_view(), name='aircraft-models-create'),
    path('aircraft-models/<uuid:aircraft_model_id>/master-components', launchpad_views.AircraftModelMasterComponents.as_view(), name='aircraft-models-detail'),
 
    path('aircraft-assemblies/<uuid:aircraft_model_id>/new', launchpad_views.AircraftAssembliesCreateView.as_view(), name='aircraft-assemblies-create'),
    path('aircraft-assemblies/<uuid:aircraft_assembly_id>/update', launchpad_views.AircraftAssembliesComponentsUpdate.as_view(), name='aircraft-assemblies-components-update'),
    path('aircraft-assemblies/<uuid:aircraft_assembly_id>/detail', launchpad_views.AircraftAssembliesDetail.as_view(), name='aircraft-assemblies-detail'),
    # path('aircraft-assemblies/<uuid:aircraft_assembly_id>', launchpad_views.AircraftAssembliesUpdate.as_view(), name='aircraft-assemblies-update'),
    path('aircraft-assemblies/<str:view_type>', launchpad_views.AircraftAssembliesList.as_view(), name='aircraft-assemblies-list'),
    path('aircraft-assemblies', launchpad_views.AircraftAssembliesList.as_view(), name='aircraft-assemblies-list'),
    
    path('incidents/<uuid:aircraft_id>/new', launchpad_views.IncidentsCreateView.as_view(), name='incidents-create'),    
    path('incidents/calendar', launchpad_views.IncidentsCalendar.as_view(), name='incidents-calendar'),
    path('incidents/<uuid:incident_id>', launchpad_views.IncidentsUpdate.as_view(), name='incidents-update'),
    path('incidents/<uuid:incident_id>/detail', launchpad_views.IncidentsDetail.as_view(), name='incidents-detail'),    
    path('incidents', launchpad_views.IncidentsList.as_view(), name='incidents-list'),
    
  
    path('aircraft-master-components', launchpad_views.AircraftMasterComponentsList.as_view(), name='aircraft-master-components-list'),
    path('aircraft-master-components/family/<int:aircraft_master_component_family>', launchpad_views.AircraftMasterComponentsFamilyList.as_view(), name='aircraft-master-components-list'),
    path('aircraft-master-components/<uuid:aircraft_master_component_id>', launchpad_views.AircraftMasterComponentsUpdate.as_view(), name='aircraft-master-components-update'),
    path('aircraft-master-components/<uuid:aircraft_master_component_id>/detail', launchpad_views.AircraftMasterComponentsDetail.as_view(), name='aircraft-master-components-detail'),
    path('aircraft-master-components/new', launchpad_views.AircraftMasterComponentsCreateView.as_view(), name='aircraft-master-components-create'),

    path('stock-keeping/<uuid:aircraft_master_component_id>', launchpad_views.AircraftMasterComponentsStockDetail.as_view(), name='aircraft-master-components-stock-keeping'),
    path('stock-keeping', launchpad_views.AircraftMasterComponentsStockDetail.as_view(), name='aircraft-master-components-stock-keeping'),
  
    path('aircraft-components/<uuid:aircraft_component_id>', launchpad_views.AircraftComponentsUpdate.as_view(), name='aircraft-components-update'),
    path('aircraft-components/<uuid:aircraft_component_id>/detail', launchpad_views.AircraftComponentsDetail.as_view(), name='aircraft-components-detail'),
    path('aircraft-components/<uuid:aircraft_component_id>/remove', launchpad_views.AircraftComponentsRemove.as_view(), name='aircraft-components-remove'),
    path('aircraft-components/<uuid:aircraft_master_component_id>/new', launchpad_views.AircraftComponentsCreateView.as_view(), name='aircraft-components-create'),
    path('aircraft-components/verify', launchpad_views.AircraftComponentsSearchView.as_view(), name='verify-aircraft-components'),
    path('aircraft-components/<str:aerobridge_id>/history', launchpad_views.AircraftComponentsHistoryView.as_view(), name='aircraft-components-history'),
    path('aircraft-components/<str:view_type>', launchpad_views.AircraftComponentsList.as_view(), name='aircraft-components-list-filtered'),    
    path('aircraft-components', launchpad_views.AircraftComponentsList.as_view(), name='aircraft-components-list'),
 
    path('companies', launchpad_views.CompaniesList.as_view(), name='companies-list'),
    path('companies/<uuid:company_id>', launchpad_views.CompaniesUpdate.as_view(), name='companies-update'),
    path('companies/<uuid:company_id>/detail', launchpad_views.CompaniesDetail.as_view(), name='companies-detail'),
    path('companies/new', launchpad_views.CompanyCreateView.as_view(), name='companies-create'),
    
    
    path('firmwares', launchpad_views.FirmwaresList.as_view(), name='firmwares-list'),
    path('firmwares/<uuid:firmware_id>', launchpad_views.FirmwaresUpdate.as_view(), name='firmwares-update'),
    path('firmwares/new', launchpad_views.FirmwareCreateView.as_view(), name='firmwares-create'),
    path('firmwares/<uuid:firmware_id>/detail', launchpad_views.FirmwaresDetail.as_view(), name='firmwares-detail'),
 
    path('flightplans', launchpad_views.FlightPlansList.as_view(), name='flightplans-list'),
    path('flightplans/<uuid:flightplan_id>', launchpad_views.FlightPlansUpdate.as_view(), name='flightplans-update'),
    path('flightplans/<uuid:flightplan_id>/detail', launchpad_views.FlightPlansDetail.as_view(), name='flightplans-detail'),
    path('flightplans/new', launchpad_views.FlightPlanCreateView.as_view(), name='flightplans-create'),
  
    path('flightoperations', launchpad_views.FlightOperationsList.as_view(), name='flightoperations-list'),
    path('flightoperations/calendar', launchpad_views.FlightOperationsCalendar.as_view(), name='flightoperations-calendar'),
    path('flightoperations/<uuid:flightoperation_id>', launchpad_views.FlightOperationsUpdate.as_view(), name='flightoperations-update'),
    path('flightoperations/<uuid:flightoperation_id>/detail', launchpad_views.FlightOperationsDetail.as_view(), name='flightoperations-detail'),
    path('flightoperations/new', launchpad_views.FlightOperationCreateView.as_view(), name='flightoperations-create'),
    path('flightoperations/<uuid:flightoperation_id>/permission', launchpad_views.FlightOperationPermissionCreateView.as_view(), name='flightoperations-permission-create'),
 
    path('flightpermissions', launchpad_views.FlightPermissionsList.as_view(), name='flightpermissions-list'),
    path('flightpermissions-read-first', launchpad_views.FlightPermissionsReadFirst.as_view(), name='flightpermissions-read-first'),
    path('flightpermissions/<uuid:flightpermission_id>/detail', launchpad_views.FlightPermissionsDetail.as_view(), name='flightpermissions-detail'),    
    
    # path('flightpermissions/new', launchpad_views.FlightPermissionCreateView.as_view(), name='flightpermissions-create'),
    # path('digitalsky-flight-permissions', launchpad_views.FlightPermissionDigitalSkyList.as_view(), name='flightpermissions-digitalsky-list'),
    # path('digitalsky-flight-permissions/thanks', launchpad_views.FlightPermissionDigitalSkyThanks.as_view(), name='flightpermissions-digitalsky-thanks'),
    # path('digitalsky-flight-permissions/<uuid:flightpermission_id>/request', launchpad_views.FlightPermissionDigitalSkyRequest.as_view(), name='flightpermissions-digitalsky-request'),
 
    path('flightlogs', launchpad_views.FlightLogsList.as_view(), name='flightlogs-list'),
    path('flightlogs/<uuid:flightlog_id>/detail', launchpad_views.FlightLogsDetail.as_view(), name='flightlogs-detail'),
    path('flightlogs/<uuid:flightlog_id>/sign', launchpad_views.FlightLogsSign.as_view(), name='flightlogs-sign-thanks'),
    path('flightlogs/<uuid:flightlog_id>', launchpad_views.FlightLogsUpdate.as_view(), name='flightlogs-update'),
    path('flightlogs/new', launchpad_views.FlightLogCreateView.as_view(), name='flightlogs-create'),

    path('signed-flightlogs', launchpad_views.SignedFlightLogsList.as_view(), name='signed-flight-logs-list'),
    path('signed-flightlogs/<uuid:signed_flightlog_id>', launchpad_views.SignedFlightLogsDetail.as_view(), name='signed-flight-logs-detail'),

    path('credentials-read-first', launchpad_views.CredentialsReadFirst.as_view(), name='credentials-list'),
    path('credentials', launchpad_views.CredentialsList.as_view(), name='credentials-list'),
    path('credentials/<uuid:credential_id>/detail', launchpad_views.CredentialsDetail.as_view(), name='credentials-detail'),
    path('credentials/<uuid:credential_id>', launchpad_views.CredentialsUpdate.as_view(), name='credentials-update'),
    path('credentials/<uuid:credential_id>/delete', launchpad_views.CredentialsDelete.as_view(), name='credentials-delete'),
    path('credentials/new', launchpad_views.CredentialsCreateView.as_view(), name='credentials-create'),
    
    path('cloud-files', launchpad_views.CloudFilesList.as_view(), name='cloud-files-list'),
    path('cloud-files/<uuid:cloudfile_id>/detail', launchpad_views.CloudFilesDetail.as_view(), name='cloud-files-detail'),
    path('cloud-files/upload', launchpad_views.CloudFilesCreateView.as_view(), name='cloud-files-upload'),
]