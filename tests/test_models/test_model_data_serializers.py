import json
import os

from digitalsky_provider.serializers import DigitalSkyLogSerializer
from gcs_operations.serializers import CloudFileSerializer, FirmwareSerializer, FlightPlanSerializer, \
    FlightOperationSerializer, FlightOperationListSerializer, FlightPermissionSerializer, FlightLogSerializer, \
    TransactionSerializer, FlightOperationPermissionSerializer, SignedFlightLogSerializer
from pki_framework.serializers import AerobridgeCredentialSerializer, AerobridgeCredentialGetSerializer, \
    AerobridgeCredentialPostSerializer
from registry.serializers import PersonSerializer, ManufacturerSerializer, AddressSerializer, AuthorizationSerializer, \
    OperatorSerializer, ContactSerializer, ContactDetailSerializer, TestsSerializer, PilotSerializer, \
    TestsValiditySerializer, TypeCertificateSerializer, AircraftSerializer, PrivilegedOperatorSerializer, \
    OperatorSelectRelatedSerializer, AircraftFullSerializer, ActivitySerializer, AircraftDetailSerializer
from .test_setup import TestModels


class TestModelDataSerializers(TestModels):
    data_path = os.getcwd() + '/tests/fixtures/'
    fixtures = ['Activity', 'Authorization', 'Address', 'Person', 'Operator', 'Test', 'Manufacturer', 'Aircraft',
                'FlightPlan', 'TypeCertificate', 'Transaction', 'Pilot', 'FlightOperation', 'FlightLog',
                'FlightPermission', 'AircraftComponent']

    def _get_data_for_model(self, model_name, index=0):
        filepath = '%s%s.json' % (self.data_path, model_name)
        if os.path.exists(filepath):
            data = json.loads(open(filepath, 'r').read())
            return data[index]['fields']
        else:
            raise AssertionError("File %s.json does not exists in fixtures" % model_name)

    def test_digitalsky_provider_digitalsky_log_data_serializer(self):
        data = self._get_data_for_model('DigitalSkyLog')
        digitalsky_log_serializer = DigitalSkyLogSerializer(data=data)
        required_keys = {'response_code', 'response', 'timestamp', 'txn'}

        self.assertTrue(digitalsky_log_serializer.is_valid())
        self.assertEqual(set(digitalsky_log_serializer.validated_data.keys()), required_keys)
        self.assertEqual(digitalsky_log_serializer.errors, dict())

    def test_gcs_operations_cloud_file_data_serializer(self):
        data = self._get_data_for_model('CloudFile')
        cloud_file_serializer = CloudFileSerializer(data=data)
        required_keys = {'upload_type', 'name', 'location'}

        self.assertTrue(cloud_file_serializer.is_valid())
        self.assertEqual(set(cloud_file_serializer.validated_data.keys()), required_keys)
        self.assertEqual(cloud_file_serializer.errors, dict())

    def test_gcs_operations_firmware_data_serializer(self):
        data = self._get_data_for_model('Firmware')
        firmware_serializer = FirmwareSerializer(data=data)
        required_keys = {'is_active', 'manufacturer', 'friendly_name', 'version', 'binary_file_url', 'public_key'}

        self.assertTrue(firmware_serializer.is_valid())
        self.assertEqual(set(firmware_serializer.validated_data.keys()), required_keys)
        self.assertEqual(firmware_serializer.errors, dict())

    def test_gcs_operations_flight_plan_data_serializer(self):
        data = self._get_data_for_model('FlightPlan')
        # plan_file_json and geo_json are JSONFields
        data['plan_file_json'] = json.loads(data['plan_file_json'])
        data['geo_json'] = json.loads(data['geo_json'])
        flight_plan_serializer = FlightPlanSerializer(data=data)
        required_keys = {'name', 'plan_file_json'}

        self.assertTrue(flight_plan_serializer.is_valid())
        self.assertEqual(set(flight_plan_serializer.validated_data.keys()), required_keys)
        self.assertEqual(flight_plan_serializer.errors, dict())

    def test_gcs_operations_flight_operation_data_serializer(self):
        data = self._get_data_for_model('FlightOperation')
        flight_operation_serializer = FlightOperationSerializer(data=data)
        required_keys = {'purpose', 'start_datetime', 'operator', 'pilot', 'name', 'flight_plan', 'type_of_operation',
                         'end_datetime', 'drone', }

        self.assertTrue(flight_operation_serializer.is_valid())
        self.assertEqual(set(flight_operation_serializer.validated_data.keys()), required_keys)
        self.assertEqual(flight_operation_serializer.errors, dict())

    def test_gcs_operations_flight_operation_list_data_serializer(self):
        data = self._get_data_for_model('FlightOperation')
        flight_operation_list_serializer = FlightOperationListSerializer(data=data)
        required_keys = {'pilot', 'purpose', 'flight_plan', 'start_datetime', 'operator', 'drone', 'type_of_operation',
                         'end_datetime', 'name', 'is_editable'}

        self.assertTrue(flight_operation_list_serializer.is_valid())
        self.assertEqual(set(flight_operation_list_serializer.validated_data.keys()), required_keys)
        self.assertEqual(flight_operation_list_serializer.errors, dict())

    def test_gcs_operations_flight_operation_permission_data_serializer(self):
        data = self._get_data_for_model('FlightOperation')
        flight_operation_permission_serializer = FlightOperationPermissionSerializer(data=data)

        self.assertTrue(flight_operation_permission_serializer.is_valid())
        # empty validated data because read-only fields
        self.assertFalse(flight_operation_permission_serializer.validated_data)
        self.assertEqual(flight_operation_permission_serializer.errors, dict())

    def test_gcs_operations_transaction_data_serializer(self):
        data = self._get_data_for_model('Transaction')
        transaction_serializer = TransactionSerializer(data=data)
        required_keys = {'prefix', 'aircraft'}

        self.assertTrue(transaction_serializer.is_valid())
        self.assertEqual(set(transaction_serializer.validated_data.keys()), required_keys)
        self.assertEqual(transaction_serializer.errors, dict())

    def test_gcs_operations_flight_permission_data_serializer(self):
        data = self._get_data_for_model('FlightPermission')
        flight_permission_serializer = FlightPermissionSerializer(data=data)
        required_keys = {'token'}

        self.assertTrue(flight_permission_serializer.is_valid())
        self.assertEqual(set(flight_permission_serializer.validated_data.keys()), required_keys)
        self.assertEqual(flight_permission_serializer.errors, dict())

    def test_gcs_operations_flight_log_data_serializer(self):
        data = self._get_data_for_model('FlightLog')
        flight_log_serializer = FlightLogSerializer(data=data)
        required_keys = {'operation', 'raw_log'}

        self.assertTrue(flight_log_serializer.is_valid())
        self.assertEqual(set(flight_log_serializer.validated_data.keys()), required_keys)
        self.assertEqual(flight_log_serializer.errors, dict())

    def test_gcs_operations_signed_flight_log_data_serializer(self):
        data = self._get_data_for_model('SignedFlightLog')
        signed_flight_log_serializer = SignedFlightLogSerializer(data=data)
        required_keys = {'raw_flight_log', 'signed_log'}

        self.assertTrue(signed_flight_log_serializer.is_valid())
        self.assertEqual(set(signed_flight_log_serializer.validated_data.keys()), required_keys)
        self.assertEqual(signed_flight_log_serializer.errors, dict())

    def test_registry_person_data_serializer(self):
        data = self._get_data_for_model('Person')
        person_serializer = PersonSerializer(data=data)
        required_keys = {'email', 'first_name', 'last_name', 'middle_name'}

        self.assertTrue(person_serializer.is_valid())
        self.assertEqual(set(person_serializer.validated_data.keys()), required_keys)
        self.assertEqual(person_serializer.errors, dict())

    def test_registry_address_data_serializer(self):
        data = self._get_data_for_model('Address')
        address_serializer = AddressSerializer(data=data)
        required_keys = {'postcode', 'address_line_1', 'address_line_2', 'address_line_3', 'city', 'country'}

        self.assertTrue(address_serializer.is_valid())
        self.assertEqual(set(address_serializer.validated_data.keys()), required_keys)
        self.assertEqual(address_serializer.errors, dict())

    def test_registry_activity_data_serializer(self):
        data = self._get_data_for_model('Activity')
        activity_serializer = ActivitySerializer(data=data)
        required_keys = {'activity_type', 'name'}

        self.assertTrue(activity_serializer.is_valid())
        self.assertEqual(set(activity_serializer.validated_data.keys()), required_keys)
        self.assertEqual(activity_serializer.errors, dict())

    def test_registry_authorization_data_serializer(self):
        data = self._get_data_for_model('Authorization')
        authorization_serializer = AuthorizationSerializer(data=data)
        required_keys = {'title', 'end_date'}

        self.assertTrue(authorization_serializer.is_valid())
        self.assertEqual(set(authorization_serializer.validated_data.keys()), required_keys)
        self.assertEqual(authorization_serializer.errors, dict())

    def test_registry_operator_data_serializer(self):
        data = self._get_data_for_model('Operator')
        operator_serializer = OperatorSerializer(data=data)
        required_keys = {'website', 'email', 'insurance_number', 'phone_number', 'country', 'operator_type',
                         'expiration', 'operational_authorizations', 'authorized_activities', 'company_name',
                         'vat_number', 'company_number', 'address'}

        self.assertTrue(operator_serializer.is_valid())
        self.assertEqual(set(operator_serializer.validated_data.keys()), required_keys)
        self.assertEqual(operator_serializer.errors, dict())

    def test_registry_privileged_operator_data_serializer(self):
        data = self._get_data_for_model('Operator')
        privileged_operator_serializer = PrivilegedOperatorSerializer(data=data)
        required_keys = {'email', 'country', 'website', 'operator_type', 'company_name'}

        self.assertTrue(privileged_operator_serializer.is_valid())
        self.assertEqual(set(privileged_operator_serializer.validated_data.keys()), required_keys)
        self.assertEqual(privileged_operator_serializer.errors, dict())

    def test_registry_operator_select_related_data_serializer(self):
        data = self._get_data_for_model('Operator')
        operator_select_related_serializer = OperatorSelectRelatedSerializer(data=data)
        required_keys = {'website', 'email', 'company_name', 'phone_number', 'country', 'operator_type',
                         'company_number'}

        self.assertTrue(operator_select_related_serializer.is_valid())
        self.assertEqual(set(operator_select_related_serializer.validated_data.keys()), required_keys)
        self.assertEqual(operator_select_related_serializer.errors, dict())

    def test_registry_contact_data_serializer(self):
        data = self._get_data_for_model('Contact')
        contact_serializer = ContactSerializer(data=data)
        required_keys = {'role_type', 'person'}

        self.assertTrue(contact_serializer.is_valid())
        self.assertEqual(set(contact_serializer.validated_data.keys()), required_keys)
        self.assertEqual(contact_serializer.errors, dict())

    def test_registry_contact_detail_data_serializer(self):
        data = self._get_data_for_model('Contact')
        contact_detail_serializer = ContactDetailSerializer(data=data)
        required_keys = {'role_type'}

        self.assertTrue(contact_detail_serializer.is_valid())
        self.assertEqual(set(contact_detail_serializer.validated_data.keys()), required_keys)
        self.assertEqual(contact_detail_serializer.errors, dict())

    def test_registry_tests_data_serializer(self):
        data = self._get_data_for_model('Test')
        test_serializer = TestsSerializer(data=data)

        self.assertTrue(test_serializer.is_valid())
        # empty validated_data since read-only fields
        self.assertFalse(test_serializer.validated_data)
        self.assertEqual(test_serializer.errors, dict())

    def test_registry_pilot_data_serializer(self):
        data = self._get_data_for_model('Pilot', index=0)
        pilot_serializer = PilotSerializer(data=data)
        required_keys = {'operator', 'is_active', 'photo', 'identification_photo'}

        self.assertTrue(pilot_serializer.is_valid())
        self.assertEqual(set(pilot_serializer.validated_data.keys()), required_keys)
        self.assertEqual(pilot_serializer.errors, dict())

    def test_registry_testValidity_data_serializer(self):
        data = self._get_data_for_model('TestValidity')
        test_validity_serializer = TestsValiditySerializer(data=data)
        required_keys = {'expiration', 'taken_at'}

        self.assertTrue(test_validity_serializer.is_valid())
        self.assertEqual(set(test_validity_serializer.validated_data.keys()), required_keys)
        self.assertEqual(test_validity_serializer.errors, dict())

    def test_registry_typeCertificate_data_serializer(self):
        data = self._get_data_for_model('TypeCertificate')
        type_certificate_serializer = TypeCertificateSerializer(data=data)
        required_keys = {'type_certificate_id', 'type_certificate_holder_country', 'type_certificate_holder',
                         'type_certificate_issuing_country'}

        self.assertTrue(type_certificate_serializer.is_valid())
        self.assertEqual(set(type_certificate_serializer.validated_data.keys()), required_keys)
        self.assertEqual(type_certificate_serializer.errors, dict())

    def test_registry_manufacturer_data_serializer(self):
        data = self._get_data_for_model('Manufacturer')
        manufacturer_serializer = ManufacturerSerializer(data=data)
        required_keys = {'role', 'full_name', 'common_name'}

        self.assertTrue(manufacturer_serializer.is_valid())
        self.assertEqual(set(manufacturer_serializer.validated_data.keys()), required_keys)
        self.assertEqual(manufacturer_serializer.errors, dict())

    def test_registry_aircraft_data_serializer(self):
        data = self._get_data_for_model('Aircraft')
        aircraft_serializer = AircraftSerializer(data=data)
        required_keys = {'flight_controller_id', 'operator', 'photo', 'category', 'flight_controller_id', 'status',
                         'manufacturer', 'name'}

        self.assertTrue(aircraft_serializer.is_valid())
        self.assertEqual(set(aircraft_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aircraft_serializer.errors, dict())

    def test_registry_aircraft_full_data_serializer(self):
        data = self._get_data_for_model('Aircraft')
        aircraft_full_serializer = AircraftFullSerializer(data=data)
        required_keys = {'name', 'manufacturer', 'operator', 'flight_controller_id', 'photo', 'category', 'status',
                         'components'}

        self.assertTrue(aircraft_full_serializer.is_valid())
        self.assertEqual(set(aircraft_full_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aircraft_full_serializer.errors, dict())

    def test_registry_aircraft_detail_data_serializer(self):
        data = self._get_data_for_model('AircraftDetail')
        aircraft_detail_serializer = AircraftDetailSerializer(data=data)
        required_keys = {'mass', 'commission_date', 'max_speed',
                         'manufactured_at', 'max_endurance', 'digital_sky_uin_number', 
                         'icao_aircraft_type_designator', 'aircraft', 'type_certificate',
                         'max_certified_takeoff_weight', 'is_registered', 'registration_mark', 'dimension_length',
                         'identification_photo', 'operating_frequency', 'max_range', 
                         'max_height_attainable', 'dimension_height', 'sub_category', 'dimension_breadth'}

        self.assertTrue(aircraft_detail_serializer.is_valid())
        self.assertEqual(set(aircraft_detail_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aircraft_detail_serializer.errors, dict())

    def test_pki_framework_aerobridge_credentials_data_serializer(self):
        data = self._get_data_for_model('AerobridgeCredential')
        aerobridge_credentials_serializer = AerobridgeCredentialSerializer(data=data)
        required_keys = {'name', 'association', 'manufacturer', 'is_active', 'aircraft', 'operator'}

        self.assertTrue(aerobridge_credentials_serializer.is_valid())
        self.assertEqual(set(aerobridge_credentials_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aerobridge_credentials_serializer.errors, dict())

    def test_pki_framweork_digitalsky_get_credentials_data_serializer(self):
        data = self._get_data_for_model('AerobridgeCredential')
        aerobridge_credentials_get_serializer = AerobridgeCredentialGetSerializer(data=data)
        required_keys = {'name', 'is_active', 'aircraft', 'operator', 'manufacturer'}

        self.assertTrue(aerobridge_credentials_get_serializer.is_valid())
        self.assertEqual(set(aerobridge_credentials_get_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aerobridge_credentials_get_serializer.errors, dict())

    def test_pki_framweork_digitalsky_post_credentials_data_serializer(self):
        data = self._get_data_for_model('AerobridgeCredential')
        aerobridge_credentials_post_serializer = AerobridgeCredentialPostSerializer(data=data)
        required_keys = {'name', 'token_type', 'token', 'association', 'manufacturer', 'is_active', 'aircraft',
                         'operator'}

        self.assertTrue(aerobridge_credentials_post_serializer.is_valid())
        self.assertEqual(set(aerobridge_credentials_post_serializer.validated_data.keys()), required_keys)
        self.assertEqual(aerobridge_credentials_post_serializer.errors, dict())
