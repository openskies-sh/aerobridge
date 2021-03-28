import json
import os

from gcs_operations.serializers import FirmwareSerializer
from launchpad.serializers import ActivitySerializer, EngineSerializer
from registry.serializers import PersonSerializer, ManufacturerSerializer, AddressSerializer, AuthorizationSerializer, \
    OperatorSerializer, ContactSerializer, ContactDetailSerializer, TestsSerializer, PilotSerializer, \
    TestsValiditySerializer, TypeCertificateSerializer, AircraftSerializer, PilotDetailSerializer, \
    AircraftSigningSerializer
from .test_setup import TestModels


class TestModelSerializers(TestModels):
    data_path = os.getcwd() + '/tests/fixtures/'
    fixtures = ['Activity', 'Authorization', 'Address', 'Person', 'Operator', 'Test', 'Manufacturer']

    def _get_data_for_model(self, model_name):
        filepath = '%s%s.json' % (self.data_path, model_name)
        if os.path.exists(filepath):
            data = json.loads(open(filepath, 'r').read())
            return data[0]['fields']
        else:
            raise AssertionError("File %s.json does not exists in fixtures" % model_name)

    def notest_digitalsky_provider_digitalsky_log_serializer(self):
        pass

    def notest_digitalsky_provider_aircraft_register_serializer(self):
        pass

    def notest_gcs_operations_flight_plan_serializer(self):
        pass
    
    def notest_gcs_operations_flight_operation_serializer(self):
        pass

    def notest_gcs_operations_transaction_serializer(self):
        pass

    def notest_gcs_operations_flight_permission_serializer(self):
        pass

    def notest_gcs_operations_flight_log_serializer(self):
        pass

    def notest_gcs_operations_uin_application_serializer(self):
        pass

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

    def test_registry_activity_serializer(self):
        data = self._get_data_for_model('Activity')
        activity_serializer = ActivitySerializer(data=data)
        self.assertTrue(activity_serializer.is_valid())
        self.assertNotEqual(activity_serializer.validated_data, dict)
        self.assertEqual(activity_serializer.errors, dict())

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

    def test_registry_test_serializer(self):
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

    def test_registry_engine_serializer(self):
        data = self._get_data_for_model('Engine')
        engine_serializer = EngineSerializer(data=data)
        self.assertTrue(engine_serializer.is_valid())
        self.assertNotEqual(engine_serializer.validated_data, dict)
        self.assertEqual(engine_serializer.errors, dict())

    def test_registry_firmware_serializer(self):
        data = self._get_data_for_model('Firmware')
        firmware_serializer = FirmwareSerializer(data=data)
        self.assertTrue(firmware_serializer.is_valid())
        self.assertNotEqual(firmware_serializer.validated_data, dict)
        self.assertEqual(firmware_serializer.errors, dict())

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
