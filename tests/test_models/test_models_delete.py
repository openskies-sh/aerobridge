from digitalsky_provider.models import DigitalSkyLog
from gcs_operations.models import CloudFile, FlightPlan, FlightOperation, Transaction, FlightPermission, FlightLog
from pki_framework.models import AerobridgeCredential
from registry.models import Person, Address, Activity, Authorization, Operator, Contact, Test, TypeCertificate, \
    Manufacturer, Firmware, Pilot, TestValidity, Aircraft
from .test_setup import TestModels


class TestModelsDelete(TestModels):
    fixtures = ['Activity', 'Address', 'Authorization', 'Manufacturer', 'Operator', 'Person', 'Test',
                'TypeCertificate', 'Pilot', 'CloudFile', 'FlightPlan', 'FlightOperation', 'Aircraft', 'Transaction',
                'Contact', 'DigitalSkyLog', 'Firmware', 'FlightLog', 'FlightPermission',
                'TestValidity', 'AerobridgeCredential']

    def test_digitalsky_provider_digitalsky_log_delete(self):
        digitalsky_log = DigitalSkyLog.objects.first()
        self.assertIsNotNone(digitalsky_log)
        digitalsky_log.delete()
        self.assertNotIn(digitalsky_log, DigitalSkyLog.objects.all())

    def test_gcs_operations_cloud_file_delete(self):
        cloud_file = CloudFile.objects.first()
        self.assertIsNotNone(cloud_file)
        cloud_file.delete()
        self.assertNotIn(cloud_file, CloudFile.objects.all())

    def test_gcs_operations_flight_plan_delete(self):
        flight_plan = FlightPlan.objects.first()
        self.assertIsNotNone(flight_plan)
        flight_plan.delete()
        self.assertNotIn(flight_plan, FlightPlan.objects.all())

    def test_gcs_operations_flight_operation_delete(self):
        flight_operation = FlightOperation.objects.first()
        self.assertIsNotNone(flight_operation)
        flight_operation.delete()
        self.assertNotIn(flight_operation, FlightOperation.objects.all())

    def test_gcs_operations_transaction_delete(self):
        transaction = Transaction.objects.first()
        self.assertIsNotNone(transaction)
        transaction.delete()
        self.assertNotIn(transaction, Transaction.objects.all())

    def test_gcs_operations_flight_permission_delete(self):
        flight_permission = FlightPermission.objects.first()
        self.assertIsNotNone(flight_permission)
        flight_permission.delete()
        self.assertNotIn(flight_permission, FlightPermission.objects.all())

    def test_gcs_operations_flight_log_delete(self):
        flight_log = FlightLog.objects.first()
        self.assertIsNotNone(flight_log)
        flight_log.delete()
        self.assertNotIn(flight_log, FlightLog.objects.all())

    def test_registry_person_delete(self):
        person = Person.objects.first()
        self.assertIsNotNone(person)
        person.delete()
        self.assertNotIn(person, Person.objects.all())

    def test_registry_address_delete(self):
        address = Address.objects.first()
        self.assertIsNotNone(address)
        address.delete()
        self.assertNotIn(address, Address.objects.all())

    def test_registry_activity_delete(self):
        activity = Activity.objects.first()
        self.assertIsNotNone(activity)
        activity.delete()
        self.assertNotIn(activity, Activity.objects.all())

    def test_registry_authorization_delete(self):
        authorization = Authorization.objects.first()
        self.assertIsNotNone(authorization)
        authorization.delete()
        self.assertNotIn(authorization, Authorization.objects.all())

    def test_registry_operator_delete(self):
        operator = Operator.objects.first()
        self.assertIsNotNone(operator)
        operator.delete()
        self.assertNotIn(operator, Operator.objects.all())

    def test_registry_contact_delete(self):
        contact = Contact.objects.first()
        self.assertIsNotNone(contact)
        contact.delete()
        self.assertNotIn(contact, Contact.objects.all())

    def test_registry_test_delete(self):
        test = Test.objects.first()
        self.assertIsNotNone(test)
        test.delete()
        self.assertNotIn(test, Test.objects.all())

    def test_registry_pilot_delete(self):
        pilot = Pilot.objects.first()
        self.assertIsNotNone(pilot)
        pilot.delete()
        self.assertNotIn(pilot, Pilot.objects.all())

    def test_registry_testValidity_delete(self):
        test_validity = TestValidity.objects.first()
        self.assertIsNotNone(test_validity)
        test_validity.delete()
        self.assertNotIn(test_validity, TestValidity.objects.all())

    def test_registry_typeCertificate_delete(self):
        type_certificate = TypeCertificate.objects.first()
        self.assertIsNotNone(type_certificate)
        type_certificate.delete()
        self.assertNotIn(type_certificate, TypeCertificate.objects.all())

    def test_registry_manufacturer_delete(self):
        manufacturer = Manufacturer.objects.first()
        self.assertIsNotNone(manufacturer)
        manufacturer.delete()
        self.assertNotIn(manufacturer, Manufacturer.objects.all())


    def test_registry_firmware_delete(self):
        firmware = Firmware.objects.first()
        self.assertIsNotNone(firmware)
        firmware.delete()
        self.assertNotIn(firmware, Firmware.objects.all())

    def test_registry_aircraft_delete(self):
        aircraft = Aircraft.objects.first()
        self.assertIsNotNone(aircraft)
        aircraft.delete()
        self.assertNotIn(aircraft, Aircraft.objects.all())

    def test_pki_framework_aerobridge_credentials_delete(self):
        aerobridge_credentials = AerobridgeCredential.objects.first()
        self.assertIsNotNone(aerobridge_credentials)
        aerobridge_credentials.delete()
        self.assertNotIn(aerobridge_credentials, Aircraft.objects.all())
