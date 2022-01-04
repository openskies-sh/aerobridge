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
    path('aircrafts/<uuid:aircraft_id>/detail', launchpad_views.AircraftDetail.as_view(), name='aircrafts-detail'),
    path('aircrafts/new', launchpad_views.AircraftCreateView.as_view(), name='aircrafts-create'),

    path('aircraft-extended', launchpad_views.AircraftExtendedList.as_view(), name='aircraft-extended-list'),
    path('aircraft-extended/<uuid:aircraft_detail_id>', launchpad_views.AircraftExtendedUpdate.as_view(), name='aircraft-extended-update'),
    path('aircraft-extended/<uuid:aircraft_detail_id>/detail', launchpad_views.AircraftExtendedDetail.as_view(), name='aircraft-extended-detail'),
    path('aircraft-extended/new', launchpad_views.AircraftExtendedCreateView.as_view(), name='aircraft-extended-create'),
 
    path('aircraft-components', launchpad_views.AircraftComponentsList.as_view(), name='aircraft-components-list'),
    path('aircraft-components/<uuid:aircraft_component_id>', launchpad_views.AircraftComponentsUpdate.as_view(), name='aircraft-components-update'),
    path('aircraft-components/<uuid:aircraft_component_id>/detail', launchpad_views.AircraftComponentsDetail.as_view(), name='aircraft-components-detail'),
    path('aircraft-components/new', launchpad_views.AircraftComponentsCreateView.as_view(), name='aircraft-components-create'),
 
    path('aircraft-components-signature', launchpad_views.AircraftComponentSignaturesList.as_view(), name='aircraft-components-signature-list'),
    path('aircraft-components/<uuid:aircraft_component_signature_id>', launchpad_views.AircraftComponentSignaturesUpdate.as_view(), name='aircraft-components-signature-update'),
    path('aircraft-components-signature/<uuid:aircraft_component_signature_id>/detail', launchpad_views.AircraftComponentSignaturesDetail.as_view(), name='aircraft-components-signature-detail'),
    path('aircraft-components-signature/new', launchpad_views.AircraftComponentSignaturesCreateView.as_view(), name='aircraft-components-signature-create'),
 
    path('manufacturers', launchpad_views.ManufacturersList.as_view(), name='manufacturers-list'),
    path('manufacturers/<uuid:manufacturer_id>', launchpad_views.ManufacturersUpdate.as_view(), name='manufacturers-update'),
    path('manufacturers/<uuid:manufacturer_id>/detail', launchpad_views.ManufacturersDetail.as_view(), name='manufacturers-detail'),
    path('manufacturers/new', launchpad_views.ManufacturerCreateView.as_view(), name='manufacturers-create'),
    
    
    path('firmwares', launchpad_views.FirmwaresList.as_view(), name='firmwares-list'),
    path('firmwares/<uuid:firmware_id>', launchpad_views.FirmwaresDetail.as_view(), name='firmwares-detail'),
    path('firmwares/new', launchpad_views.FirmwareCreateView.as_view(), name='firmwares-create'),
 
    path('flightplans', launchpad_views.FlightPlansList.as_view(), name='flightplans-list'),
    path('flightplans/<uuid:flightplan_id>', launchpad_views.FlightPlansUpdate.as_view(), name='flightplans-update'),
    path('flightplans/<uuid:flightplan_id>/detail', launchpad_views.FlightPlansDetail.as_view(), name='flightplans-detail'),
    path('flightplans/new', launchpad_views.FlightPlanCreateView.as_view(), name='flightplans-create'),
  
    path('flightoperations', launchpad_views.FlightOperationsList.as_view(), name='flightoperations-list'),
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