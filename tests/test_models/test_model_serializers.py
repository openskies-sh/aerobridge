import json
import os

from digitalsky_provider.serializers import DigitalSkyLogSerializer
from gcs_operations.serializers import FirmwareSerializer, FlightPlanSerializer, \
    FlightPlanListSerializer, FlightOperationSerializer, FlightOperationListSerializer, FlightPermissionSerializer, \
    TransactionSerializer, FlightLogSerializer
from pki_framework.serializers import AerobridgeCredentialSerializer, AerobridgeCredentialGetSerializer
from registry.serializers import PersonSerializer, ManufacturerSerializer, AddressSerializer, AuthorizationSerializer, \
    OperatorSerializer, ContactSerializer, ContactDetailSerializer, TestsSerializer, PilotSerializer, \
    TestsValiditySerializer, TypeCertificateSerializer, AircraftSerializer, PilotDetailSerializer, \
    AircraftSigningSerializer, PrivilegedOperatorSerializer, OperatorSelectRelatedSerializer, AircraftDetailSerializer
from .test_setup import TestModels


class TestModelSerializers(TestModels):
    data_path = os.getcwd() + '/tests/fixtures/'
    fixtures = ['Activity', 'Authorization', 'Address', 'Person', 'Operator', 'Test', 'Manufacturer', 'Aircraft',
                'FlightPlan', 'Engine', 'TypeCertificate', 'FlightOperation', 'Transaction']

    def _get_data_for_model(self, model_name):
        filepath = '%s%s.json' % (self.data_path, model_name)
        if os.path.exists(filepath):
            data = json.loads(open(filepath, 'r').read())
            return data[0]['fields']
        else:
            raise AssertionError("File %s.json does not exists in fixtures" % model_name)

    def test_digitalsky_provider_digitalsky_log_serializer(self):
        data = self._get_data_for_model('DigitalSkyLog')
        digitalsky_log_serializer = DigitalSkyLogSerializer(data=data)
        self.assertTrue(digitalsky_log_serializer.is_valid())
        self.assertNotEqual(digitalsky_log_serializer.validated_data, dict)
        self.assertEqual(digitalsky_log_serializer.errors, dict())

    def test_gcs_operations_firmware_serializer(self):
        data = self._get_data_for_model('Firmware')
        firmware_serializer = FirmwareSerializer(data=data)
        self.assertTrue(firmware_serializer.is_valid())
        self.assertNotEqual(firmware_serializer.validated_data, dict)
        self.assertEqual(firmware_serializer.errors, dict())

    def test_gcs_operations_flight_plan_serializer(self):
        data = self._get_data_for_model('FlightPlan')
        flight_plan_serializer = FlightPlanSerializer(data=data)
        self.assertTrue(flight_plan_serializer.is_valid())
        self.assertNotEqual(flight_plan_serializer.validated_data, dict)
        self.assertEqual(flight_plan_serializer.errors, dict())

    def test_gcs_operations_flight_plan_list_serializer(self):
        data = self._get_data_for_model('FlightPlan')
        flight_plan_list_serializer = FlightPlanListSerializer(data=data)
        self.assertTrue(flight_plan_list_serializer.is_valid())
        self.assertNotEqual(flight_plan_list_serializer.validated_data, dict)
        self.assertEqual(flight_plan_list_serializer.errors, dict())

    def test_gcs_operations_flight_operation_serializer(self):
        data = self._get_data_for_model('FlightOperation')
        flight_operation_serializer = FlightOperationSerializer(data=data)
        self.assertTrue(flight_operation_serializer.is_valid())
        self.assertNotEqual(flight_operation_serializer.validated_data, dict)
        self.assertEqual(flight_operation_serializer.errors, dict())

    def test_gcs_operations_flight_operation_list_serializer(self):
        data = self._get_data_for_model('FlightOperation')
        flight_operation_list_serializer = FlightOperationListSerializer(data=data)
        self.assertTrue(flight_operation_list_serializer.is_valid())
        self.assertNotEqual(flight_operation_list_serializer.validated_data, dict)
        self.assertEqual(flight_operation_list_serializer.errors, dict())

    def test_gcs_operations_transaction_serializer(self):
        data = self._get_data_for_model('Transaction')
        transaction_serializer = TransactionSerializer(data=data)
        self.assertTrue(transaction_serializer.is_valid())
        self.assertNotEqual(transaction_serializer.validated_data, dict)
        self.assertEqual(transaction_serializer.errors, dict())

    def test_gcs_operations_flight_permission_serializer(self):
        data = self._get_data_for_model('FlightPermission')
        flight_permission_serializer = FlightPermissionSerializer(data=data)
        self.assertTrue(flight_permission_serializer.is_valid())
        self.assertNotEqual(flight_permission_serializer.validated_data, dict)
        self.assertEqual(flight_permission_serializer.errors, dict())

    def test_gcs_operations_flight_log_serializer(self):
        data = self._get_data_for_model('FlightLog')
        flight_log_serializer = FlightLogSerializer(data=data)
        self.assertTrue(flight_log_serializer.is_valid())
        self.assertNotEqual(flight_log_serializer.validated_data, dict)
        self.assertEqual(flight_log_serializer.errors, dict())

    def test_registry_person_serializer(self):
        data = self._get_data_for_model('Person')
        person_serializer = PersonSerializer(data=data)
        self.assertTrue(person_serializer.is_valid())
        self.assertNotEqual(person_serializer.validated_data, dict)
        self.assertEqual(person_serializer.errors, dict())

    def test_registry_address_serializer(self):
        data = self._get_data_for_model('Address')
        address_serializer = AddressSerializer(data=data)
        self.assertTrue(address_serializer.is_valid())
        self.assertNotEqual(address_serializer.validated_data, dict)
        self.assertEqual(address_serializer.errors, dict())

    def test_registry_authorization_serializer(self):
        data = self._get_data_for_model('Authorization')
        authorization_serializer = AuthorizationSerializer(data=data)
        self.assertTrue(authorization_serializer.is_valid())
        self.assertNotEqual(authorization_serializer.validated_data, dict)
        self.assertEqual(authorization_serializer.errors, dict())

    def test_registry_operator_serializer(self):
        data = self._get_data_for_model('Operator')
        operator_serializer = OperatorSerializer(data=data)
        self.assertTrue(operator_serializer.is_valid())
        self.assertNotEqual(operator_serializer.validated_data, dict)
        self.assertEqual(operator_serializer.errors, dict())

    def test_registry_privileged_operator_serializer(self):
        data = self._get_data_for_model('Operator')
        privileged_operator_serializer = PrivilegedOperatorSerializer(data=data)
        self.assertTrue(privileged_operator_serializer.is_valid())
        self.assertNotEqual(privileged_operator_serializer.validated_data, dict)
        self.assertEqual(privileged_operator_serializer.errors, dict())

    def test_registry_operator_select_related_serializer(self):
        data = self._get_data_for_model('Operator')
        operator_select_related_serializer = OperatorSelectRelatedSerializer(data=data)
        self.assertTrue(operator_select_related_serializer.is_valid())
        self.assertNotEqual(operator_select_related_serializer.validated_data, dict)
        self.assertEqual(operator_select_related_serializer.errors, dict())

    def test_registry_contact_serializer(self):
        data = self._get_data_for_model('Contact')
        contact_serializer = ContactSerializer(data=data)
        self.assertTrue(contact_serializer.is_valid())
        self.assertNotEqual(contact_serializer.validated_data, dict)
        self.assertEqual(contact_serializer.errors, dict())

    def test_registry_contact_detail_serializer(self):
        data = self._get_data_for_model('Contact')
        contact_detail_serializer = ContactDetailSerializer(data=data)
        self.assertTrue(contact_detail_serializer.is_valid())
        self.assertNotEqual(contact_detail_serializer.validated_data, dict)
        self.assertEqual(contact_detail_serializer.errors, dict())

    def test_registry_tests_serializer(self):
        data = self._get_data_for_model('Test')
        test_serializer = TestsSerializer(data=data)
        self.assertTrue(test_serializer.is_valid())
        self.assertNotEqual(test_serializer.validated_data, dict)
        self.assertEqual(test_serializer.errors, dict())

    def test_registry_pilot_serializer(self):
        data = self._get_data_for_model('Pilot')
        pilot_serializer = PilotSerializer(data=data)
        self.assertTrue(pilot_serializer.is_valid())
        self.assertNotEqual(pilot_serializer.validated_data, dict)
        self.assertEqual(pilot_serializer.errors, dict())

    def test_registry_pilot_detail_serializer(self):
        data = self._get_data_for_model('Pilot')
        pilot_detail_serializer = PilotDetailSerializer(data=data)
        self.assertTrue(pilot_detail_serializer.is_valid())
        self.assertNotEqual(pilot_detail_serializer.validated_data, dict)
        self.assertEqual(pilot_detail_serializer.errors, dict())

    def test_registry_testValidity_serializer(self):
        data = self._get_data_for_model('TestValidity')
        test_validity_serializer = TestsValiditySerializer(data=data)
        self.assertTrue(test_validity_serializer.is_valid())
        self.assertNotEqual(test_validity_serializer.validated_data, dict)
        self.assertEqual(test_validity_serializer.errors, dict())

    def test_registry_typeCertificate_serializer(self):
        data = self._get_data_for_model('TypeCertificate')
        type_certificate_serializer = TypeCertificateSerializer(data=data)
        self.assertTrue(type_certificate_serializer.is_valid())
        self.assertNotEqual(type_certificate_serializer.validated_data, dict)
        self.assertEqual(type_certificate_serializer.errors, dict())

    def test_registry_manufacturer_serializer(self):
        data = self._get_data_for_model('Manufacturer')
        manufacturer_serializer = ManufacturerSerializer(data=data)
        self.assertTrue(manufacturer_serializer.is_valid())
        self.assertNotEqual(manufacturer_serializer.validated_data, dict)
        self.assertEqual(manufacturer_serializer.errors, dict())

    def test_registry_aircraft_serializer(self):
        data = self._get_data_for_model('Aircraft')
        aircraft_serializer = AircraftSerializer(data=data)
        self.assertTrue(aircraft_serializer.is_valid())
        self.assertNotEqual(aircraft_serializer.validated_data, dict)
        self.assertEqual(aircraft_serializer.errors, dict())

    def test_registry_aircraft_signing_serializer(self):
        data = self._get_data_for_model('Aircraft')
        aircraft_signing_serializer = AircraftSigningSerializer(data=data)
        self.assertTrue(aircraft_signing_serializer.is_valid())
        self.assertNotEqual(aircraft_signing_serializer.validated_data, dict)
        self.assertEqual(aircraft_signing_serializer.errors, dict())

    def test_registry_aircraft_detail_serializer(self):
        data = self._get_data_for_model('Aircraft')
        aircraft_detail_serializer = AircraftDetailSerializer(data=data)
        self.assertTrue(aircraft_detail_serializer.is_valid())
        self.assertNotEqual(aircraft_detail_serializer.validated_data, dict)
        self.assertEqual(aircraft_detail_serializer.errors, dict())

    def test_pki_framework_aerobridge_credentials_serializer(self):
        data = self._get_data_for_model('AerobridgeCredential')
        aerobridge_credentials_serializer = AerobridgeCredentialSerializer(data=data)
        self.assertTrue(aerobridge_credentials_serializer.is_valid())
        self.assertNotEqual(aerobridge_credentials_serializer.validated_data, dict)
        self.assertEqual(aerobridge_credentials_serializer.errors, dict())

    def test_pki_framweork_digitalsky_get_credentials_serializer(self):
        data = self._get_data_for_model('AerobridgeCredential')
        aerobridge_credentials_get_serializer = AerobridgeCredentialGetSerializer(data=data)
        self.assertTrue(aerobridge_credentials_get_serializer.is_valid())
        self.assertNotEqual(aerobridge_credentials_get_serializer.validated_data, dict)
        self.assertEqual(aerobridge_credentials_get_serializer.errors, dict())
