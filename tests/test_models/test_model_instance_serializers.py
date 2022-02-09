from digitalsky_provider.models import DigitalSkyLog
from digitalsky_provider.serializers import DigitalSkyLogSerializer
from gcs_operations.models import CloudFile, FlightPlan, FlightOperation, Transaction, FlightPermission, \
    SignedFlightLog, FlightLog
from gcs_operations.serializers import CloudFileSerializer, FirmwareSerializer, FlightPlanSerializer, \
    FlightOperationSerializer, FlightOperationListSerializer, FlightPermissionSerializer, FlightLogSerializer, \
    TransactionSerializer, FlightOperationPermissionSerializer, SignedFlightLogSerializer
from pki_framework.models import AerobridgeCredential
from pki_framework.serializers import AerobridgeCredentialSerializer, AerobridgeCredentialGetSerializer, \
    AerobridgeCredentialPostSerializer
from registry.models import Firmware, Person, Address, Activity, Authorization, Operator, Contact, Pilot, Test, \
    TestValidity, TypeCertificate, Manufacturer, Aircraft, AircraftDetail
from registry.serializers import PersonSerializer, ManufacturerSerializer, AddressSerializer, AuthorizationSerializer, \
    OperatorSerializer, ContactSerializer, ContactDetailSerializer, TestsSerializer, PilotSerializer, \
    TestsValiditySerializer, TypeCertificateSerializer, AircraftSerializer, PrivilegedOperatorSerializer, \
    OperatorSelectRelatedSerializer, AircraftFullSerializer, ActivitySerializer, AircraftDetailSerializer
from .test_setup import TestModels


class TestModelInstanceSerializers(TestModels):
    fixtures = ['Activity', 'Address', 'Authorization', 'Manufacturer', 'Operator', 'Person', 'Test',
                'TypeCertificate', 'Pilot', 'CloudFile', 'FlightPlan', 'FlightOperation', 'Aircraft', 'Transaction',
                'Contact', 'DigitalSkyLog', 'Firmware', 'FlightLog', 'FlightPermission', 'TestValidity',
                'AerobridgeCredential', 'SignedFlightLog', 'AircraftDetail', 'AircraftComponent']

    def setUp(self):
        self.fix_fixtures_data()

    def test_digitalsky_provider_digitalsky_log_instance_serializer(self):
        digitalsky_log_serializer = DigitalSkyLogSerializer(instance=DigitalSkyLog.objects.first())
        required_keys = {'id', 'response_code', 'response', 'timestamp', 'txn', 'updated_at'}
        self.assertEqual(set(digitalsky_log_serializer.data.keys()), required_keys)

    def test_gcs_operations_cloud_file_instance_serializer(self):
        cloud_file_serializer = CloudFileSerializer(instance=CloudFile.objects.first())
        required_keys = {'id', 'upload_type', 'name', 'location', 'created_at', 'updated_at'}
        self.assertEqual(set(cloud_file_serializer.data.keys()), required_keys)

    def test_gcs_operations_firmware_instance_serializer(self):
        firmware_serializer = FirmwareSerializer(instance=Firmware.objects.first())
        required_keys = {'id', 'is_active', 'updated_at', 'manufacturer', 'friendly_name', 'created_at', 'version',
                         'binary_file_url', 'public_key'}
        self.assertEqual(set(firmware_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_plan_instance_serializer(self):
        flight_plan_serializer = FlightPlanSerializer(instance=FlightPlan.objects.first())
        required_keys = {'id', 'updated_at', 'name', 'plan_file_json', 'created_at'}
        self.assertEqual(set(flight_plan_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_operation_instance_serializer(self):
        flight_operation_serializer = FlightOperationSerializer(instance=FlightOperation.objects.first())
        required_keys = {'id', 'purpose', 'start_datetime', 'operator', 'pilot', 'name', 'created_at', 'flight_plan',
                         'type_of_operation', 'end_datetime', 'drone', }
        self.assertEqual(set(flight_operation_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_operation_list_instance_serializer(self):
        flight_operation_list_serializer = FlightOperationListSerializer(instance=FlightOperation.objects.first())
        required_keys = {'id', 'pilot', 'purpose', 'flight_plan', 'start_datetime', 'operator', 'created_at', 'drone',
                         'type_of_operation', 'end_datetime', 'name', 'is_editable'}
        self.assertEqual(set(flight_operation_list_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_operation_permission_instance_serializer(self):
        flight_operation_permission_serializer = FlightOperationPermissionSerializer(
            instance=FlightOperation.objects.first())
        required_keys = {'operation_id', 'permission'}
        self.assertEqual(set(flight_operation_permission_serializer.data.keys()), required_keys)

    def test_gcs_operations_transaction_instance_serializer(self):
        transaction_serializer = TransactionSerializer(instance=Transaction.objects.first())
        required_keys = {'id', 'prefix', 'updated_at', 'created_at', 'aircraft'}
        self.assertEqual(set(transaction_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_permission_instance_serializer(self):
        flight_permission_serializer = FlightPermissionSerializer(instance=FlightPermission.objects.first())
        required_keys = {'id', 'updated_at', 'operation', 'status_code', 'token', 'created_at'}
        self.assertEqual(set(flight_permission_serializer.data.keys()), required_keys)

    def test_gcs_operations_flight_log_instance_serializer(self):
        flight_log_serializer = FlightLogSerializer(instance=FlightLog.objects.first())
        required_keys = {'id', 'updated_at', 'operation', 'raw_log', 'created_at'}
        self.assertEqual(set(flight_log_serializer.data.keys()), required_keys)

    def test_gcs_operations_signed_flight_log_instance_serializer(self):
        signed_flight_log_serializer = SignedFlightLogSerializer(instance=SignedFlightLog.objects.first())
        required_keys = {'id', 'raw_flight_log', 'updated_at', 'created_at', 'signed_log'}
        self.assertEqual(set(signed_flight_log_serializer.data.keys()), required_keys)

    def test_registry_person_instance_serializer(self):
        person_serializer = PersonSerializer(instance=Person.objects.first())
        required_keys = {'id', 'email', 'first_name', 'last_name', 'middle_name', 'updated_at', 'created_at'}
        self.assertEqual(set(person_serializer.data.keys()), required_keys)

    def test_registry_address_instance_serializer(self):
        address_serializer = AddressSerializer(instance=Address.objects.first())
        required_keys = {'id', 'postcode', 'updated_at', 'address_line_1', 'address_line_2', 'address_line_3', 'city',
                         'country', 'created_at'}
        self.assertEqual(set(address_serializer.data.keys()), required_keys)

    def test_registry_activity_instance_serializer(self):
        activity_serializer = ActivitySerializer(instance=Activity.objects.first())
        required_keys = {'id', 'activity_type', 'updated_at', 'created_at', 'name'}
        self.assertEqual(set(activity_serializer.data.keys()), required_keys)

    def test_registry_authorization_instance_serializer(self):
        authorization_serializer = AuthorizationSerializer(instance=Authorization.objects.first())
        required_keys = {'authorization_type', 'operation_area_type', 'end_date', 'risk_type', 'title'}
        self.assertEqual(set(authorization_serializer.data.keys()), required_keys)

    def test_registry_operator_instance_serializer(self):
        operator_serializer = OperatorSerializer(instance=Operator.objects.first())
        required_keys = {'id', 'website', 'created_at', 'email', 'insurance_number', 'phone_number', 'updated_at',
                         'country', 'operator_type', 'expiration', 'operational_authorizations',
                         'authorized_activities', 'company_name', 'vat_number', 'company_number', 'address'}
        self.assertEqual(set(operator_serializer.data.keys()), required_keys)

    def test_registry_privileged_operator_instance_serializer(self):
        privileged_operator_serializer = PrivilegedOperatorSerializer(instance=Operator.objects.first())
        required_keys = {'id', 'email', 'operational_authorizations', 'country', 'website', 'address', 'created_at',
                         'operator_type', 'company_name', 'authorized_activities', 'updated_at'}
        self.assertEqual(set(privileged_operator_serializer.data.keys()), required_keys)

    def test_registry_operator_select_related_instance_serializer(self):
        operator_select_related_serializer = OperatorSelectRelatedSerializer(instance=Operator.objects.first())
        required_keys = {'id', 'website', 'contacts', 'email', 'company_name', 'phone_number', 'updated_at', 'country',
                         'pilots', 'operator_type', 'operational_authorizations', 'created_at', 'authorized_activities',
                         'aircrafts', 'company_number', 'address'}
        self.assertEqual(set(operator_select_related_serializer.data.keys()), required_keys)

    def test_registry_contact_instance_serializer(self):
        contact_serializer = ContactSerializer(instance=Contact.objects.first())
        required_keys = {'id', 'role_type', 'updated_at', 'person'}
        self.assertEqual(set(contact_serializer.data.keys()), required_keys)

    def test_registry_contact_detail_instance_serializer(self):
        contact_detail_serializer = ContactDetailSerializer(instance=Contact.objects.first())
        required_keys = {'id', 'updated_at', 'person', 'role_type', 'operator'}
        self.assertEqual(set(contact_detail_serializer.data.keys()), required_keys)

    def test_registry_tests_instance_serializer(self):
        test_serializer = TestsSerializer(instance=Test.objects.first())
        required_keys = {'id', 'updated_at', 'taken_at', 'created_at', 'test_type'}
        self.assertEqual(set(test_serializer.data.keys()), required_keys)

    def test_registry_pilot_instance_serializer(self):
        pilot_serializer = PilotSerializer(instance=Pilot.objects.first())
        required_keys = {'id', 'operator', 'is_active', 'photo', 'address', 'tests', 'identification_photo', 'person'}
        self.assertEqual(set(pilot_serializer.data.keys()), required_keys)

    def test_registry_testValidity_instance_serializer(self):
        test_validity_serializer = TestsValiditySerializer(instance=TestValidity.objects.first())
        required_keys = {'id', 'expiration', 'taken_at', 'pilot'}
        self.assertEqual(set(test_validity_serializer.data.keys()), required_keys)

    def test_registry_typeCertificate_instance_serializer(self):
        type_certificate_serializer = TypeCertificateSerializer(instance=TypeCertificate.objects.first())
        required_keys = {'id', 'type_certificate_id', 'type_certificate_holder_country', 'type_certificate_holder',
                         'type_certificate_issuing_country'}
        self.assertEqual(set(type_certificate_serializer.data.keys()), required_keys)

    def test_registry_manufacturer_instance_serializer(self):
        manufacturer_serializer = ManufacturerSerializer(instance=Manufacturer.objects.first())
        required_keys = {'id', 'role', 'address', 'full_name', 'common_name'}
        self.assertEqual(set(manufacturer_serializer.data.keys()), required_keys)

    def test_registry_aircraft_instance_serializer(self):
        aircraft_serializer = AircraftSerializer(instance=Aircraft.objects.first())
        required_keys = {'id', 'flight_controller_id', 'operator', 'photo', 'category', 'flight_controller_id',
                         'status', 'manufacturer', 'name'}
        self.assertEqual(set(aircraft_serializer.data.keys()), required_keys)

    def test_registry_aircraft_full_instance_serializer(self):
        aircraft_full_serializer = AircraftFullSerializer(instance=Aircraft.objects.first())
        required_keys = {'id', 'name', 'manufacturer', 'operator', 'updated_at', 'flight_controller_id', 'photo',
                         'category', 'status', 'components', 'created_at'}
        self.assertEqual(set(aircraft_full_serializer.data.keys()), required_keys)

    def test_registry_aircraft_detail_instance_serializer(self):
        aircraft_detail_serializer = AircraftDetailSerializer(instance=AircraftDetail.objects.first())
        required_keys = {'id', 'mass', 'commission_date', 'max_speed',
                         'created_at', 'manufactured_at', 'max_endurance', 'digital_sky_uin_number', 
                         'icao_aircraft_type_designator', 'aircraft', 'updated_at', 'type_certificate',
                         'max_certified_takeoff_weight', 'is_registered', 'registration_mark', 'dimension_length',
                         'identification_photo',  'operating_frequency', 'max_range',
                         'max_height_attainable', 'dimension_height', 'sub_category', 'dimension_breadth'}
        self.assertEqual(set(aircraft_detail_serializer.data.keys()), required_keys)

    def test_pki_framework_aerobridge_credentials_instance_serializer(self):
        aerobridge_credentials_serializer = AerobridgeCredentialSerializer(
            instance=AerobridgeCredential.objects.first())
        required_keys = {'id', 'name', 'token_type', 'token', 'extension', 'association', 'manufacturer', 'is_active',
                         'aircraft', 'operator'}
        self.assertEqual(set(aerobridge_credentials_serializer.data.keys()), required_keys)

    def test_pki_framework_digitalsky_get_credentials_instance_serializer(self):
        aerobridge_credentials_get_serializer = AerobridgeCredentialGetSerializer(
            instance=AerobridgeCredential.objects.first())
        required_keys = {'id', 'name', 'token_type', 'extension', 'is_active', 'aircraft', 'operator', 'manufacturer',
                         'association', 'created_at'}
        self.assertEqual(set(aerobridge_credentials_get_serializer.data.keys()), required_keys)

    def test_pki_framework_digitalsky_post_credentials_instance_serializer(self):
        aerobridge_credentials_post_serializer = AerobridgeCredentialPostSerializer(
            instance=AerobridgeCredential.objects.first())
        required_keys = {'id', 'name', 'token_type', 'token', 'extension', 'association', 'manufacturer', 'is_active',
                         'aircraft', 'operator'}
        self.assertEqual(set(aerobridge_credentials_post_serializer.data.keys()), required_keys)
