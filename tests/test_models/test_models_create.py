import pytz
from django.utils import timezone

from digitalsky_provider.models import DigitalSkyLog
from gcs_operations.models import CloudFile, FlightPlan, FlightOperation, Transaction, FlightPermission, FlightLog, \
    SignedFlightLog
from pki_framework.models import AerobridgeCredential
from registry.models import Person, Address, Activity, Authorization, Operator, Contact, Test, TypeCertificate, \
    Manufacturer, Firmware, Pilot, TestValidity, Aircraft, AircraftDetail, AircraftComponent, AircraftComponentSignature
from .test_setup import TestModels


class TestModelsCreate(TestModels):
    fixtures = ['Activity', 'Address', 'Authorization', 'Person', 'Test', 'TypeCertificate', 'Operator', 'Pilot',
                'Manufacturer', 'Aircraft', 'FlightPlan', 'FlightOperation', 'Transaction', 'FlightLog',
                'AircraftComponent']

    def test_digitalsky_provider_digitalsky_log_create(self):
        digitalsky_log = DigitalSkyLog(txn=Transaction.objects.first(), response_code=self.faker.numerify('###'),
                                       response=self.faker.sentence(), timestamp=timezone.now())
        self.assertNotIn(digitalsky_log, DigitalSkyLog.objects.all())
        digitalsky_log.save()
        self.assertIn(digitalsky_log, DigitalSkyLog.objects.all())
        self.assertEqual(digitalsky_log.txn, Transaction.objects.first())

    def test_gcs_operations_cloud_file_create(self):
        cloud_file = CloudFile(location=self.faker.uri(), name=self.faker.file_name(category='text'))
        self.assertNotIn(cloud_file, CloudFile.objects.all())
        cloud_file.save()
        self.assertIn(cloud_file, CloudFile.objects.all())

    def test_gcs_operations_flight_plan_create(self):
        flight_plan = FlightPlan(name=self.faker.word(), plan_file_json=self.faker.pydict(value_types=str),
                                 geo_json=self.faker.pydict(value_types=str), is_editable=self.faker.boolean())
        self.assertNotIn(flight_plan, FlightPlan.objects.all())
        flight_plan.save()
        self.assertIn(flight_plan, FlightPlan.objects.all())

    def test_gcs_operations_flight_operation_create(self):
        flight_operation = FlightOperation(name=self.faker.word(), drone=Aircraft.objects.first(),
                                           flight_plan=FlightPlan.objects.first(), operator=Operator.objects.first(),
                                           pilot=Pilot.objects.first(), purpose=Activity.objects.first(),
                                           is_editable=self.faker.boolean(), type_of_operation=self.faker.pyint(
                min_value=0, max_value=len(FlightOperation.OPERATION_TYPES) - 1))
        self.assertNotIn(flight_operation, FlightOperation.objects.all())
        flight_operation.save()
        self.assertIn(flight_operation, FlightOperation.objects.all())
        self.assertEqual(flight_operation.drone, Aircraft.objects.first())
        self.assertEqual(flight_operation.flight_plan, FlightPlan.objects.first())
        self.assertEqual(flight_operation.purpose, Activity.objects.first())
        self.assertEqual(flight_operation.operator, Operator.objects.first())
        self.assertEqual(flight_operation.pilot, Pilot.objects.first())

    def test_gcs_operations_transaction_create(self):
        transaction = Transaction(prefix=self.faker.word(), aircraft=Aircraft.objects.first())
        self.assertNotIn(transaction, Transaction.objects.all())
        transaction.save()
        self.assertIn(transaction, Transaction.objects.all())
        self.assertEqual(transaction.aircraft, Aircraft.objects.first())

    def test_gcs_operations_flight_permission_create(self):
        flight_permission = FlightPermission(operation=FlightOperation.objects.first(), token=self.faker.json())
        self.assertNotIn(flight_permission, FlightPermission.objects.all())
        flight_permission.save()
        self.assertIn(flight_permission, FlightPermission.objects.all())
        self.assertEqual(flight_permission.operation, FlightOperation.objects.first())

    def test_gcs_operations_flight_log_create(self):
        flight_log = FlightLog(operation=FlightOperation.objects.first(), raw_log=self.faker.pydict(value_types=str),
                               is_submitted=True, is_editable=self.faker.boolean())
        self.assertNotIn(flight_log, FlightLog.objects.all())
        flight_log.save()
        self.assertIn(flight_log, FlightLog.objects.all())
        self.assertEqual(flight_log.operation, FlightOperation.objects.first())

    def test_gcs_operations_signed_flight_log_create(self):
        signed_flight_log = SignedFlightLog(raw_flight_log=FlightLog.objects.first(), signed_log=self.faker.text())
        self.assertNotIn(signed_flight_log, SignedFlightLog.objects.all())
        signed_flight_log.save()
        self.assertIn(signed_flight_log, SignedFlightLog.objects.all())
        self.assertEqual(signed_flight_log.raw_flight_log, FlightLog.objects.first())

    def test_registry_person_create(self):
        person = Person(first_name=self.faker.first_name(), last_name=self.faker.last_name(), email=self.faker.email(),
                        phone_number=self.faker.numerify('+' + '#' * 9),
                        social_security_number=self.faker.ssn(), date_of_birth=self.faker.date_of_birth())
        self.assertNotIn(person, Person.objects.all())
        person.save()
        self.assertIn(person, Person.objects.all())

    def test_registry_address_create(self):
        fake_address = self.faker.address().split('\n')
        address = Address(address_line_1=fake_address[0], address_line_2=fake_address[1],
                          postcode=self.faker.postcode(), city=self.faker.city(), state=self.faker.state(),
                          country='IN')
        self.assertNotIn(address, Address.objects.all())
        address.save()
        self.assertIn(address, Address.objects.all())

    def test_registry_activity_create(self):
        activity = Activity(name=self.faker.word(), activity_type=self.faker.pyint(min_value=0, max_value=len(
            Activity.ACTIVITYTYPE_CHOICES) - 1))
        self.assertNotIn(activity, Activity.objects.all())
        activity.save()
        self.assertIn(activity, Activity.objects.all())

    def test_registry_authorization_create(self):
        authorization = Authorization(title=self.faker.sentence(), operation_max_height=self.faker.pyint(),
                                      operation_altitude_system=self.faker.pyint(min_value=0, max_value=len(
                                          Authorization.ALTITUDE_SYSTEM) - 1),
                                      airspace_type=self.faker.pyint(min_value=0, max_value=len(
                                          Authorization.AIRSPACE_CHOICES) - 1),
                                      permit_to_fly_above_crowd=self.faker.pybool(),
                                      operation_area_type=self.faker.pyint(min_value=0, max_value=len(
                                          Authorization.AREATYPE_CHOICES) - 1),
                                      risk_type=self.faker.pyint(min_value=0, max_value=len(
                                          Authorization.RISKCLASS_CHOICES) - 1),
                                      authorization_type=self.faker.pyint(min_value=0, max_value=len(
                                          Authorization.AUTHTYPE_CHOICES) - 1))
        self.assertNotIn(authorization, Authorization.objects.all())
        authorization.save()
        self.assertIn(authorization, Authorization.objects.all())

    def test_registry_operator_create(self):
        operator = Operator(company=self.faker.uuid4(), website=self.faker.url(),
                            email=self.faker.company_email(),
                            phone_number=self.faker.numerify('+' + '#' * 9),
                            operator_type=self.faker.pyint(min_value=0, max_value=len(
                                Operator.OPTYPE_CHOICES) - 1), address=Address.objects.first(),
                            vat_number=self.faker.numerify('#' * 10),
                            insurance_number=self.faker.numerify('#' * 15), country='IN')
        self.assertNotIn(operator, Operator.objects.all())
        operator.save()
        self.assertIn(operator, Operator.objects.all())
        self.assertEqual(operator.address, Address.objects.first())
        self.assertNotIn(Authorization.objects.first(), operator.operational_authorizations.all())
        operator.operational_authorizations.add(Authorization.objects.first())
        self.assertIn(Authorization.objects.first(), operator.operational_authorizations.all())
        self.assertNotIn(Activity.objects.first(), operator.authorized_activities.all())
        operator.authorized_activities.add(Activity.objects.first())
        self.assertIn(Activity.objects.first(), operator.authorized_activities.all())

    def test_registry_contact_create(self):
        contact = Contact(operator=Operator.objects.first(), person=Person.objects.first(),
                          address=Address.objects.first(),
                          role_type=self.faker.pyint(min_value=0, max_value=len(Contact.ROLE_CHOICES) - 1))
        self.assertNotIn(contact, Contact.objects.all())
        contact.save()
        self.assertIn(contact, Contact.objects.all())
        self.assertEqual(contact.operator, Operator.objects.first())
        self.assertEqual(contact.person, Person.objects.first())
        self.assertEqual(contact.address, Address.objects.first())

    def test_registry_test_create(self):
        test = Test(test_type=self.faker.pyint(min_value=0, max_value=len(Test.TESTTYPE_CHOICES) - 1),
                    taken_at=self.faker.pyint(min_value=0, max_value=len(Test.TAKEN_AT_CHOICES) - 1),
                    name=self.faker.name())
        self.assertNotIn(test, Test.objects.all())
        test.save()
        self.assertIn(test, Test.objects.all())

    def test_registry_pilot_create(self):
        pilot = Pilot(operator=Operator.objects.first(), person=Person.objects.first(), photo=self.faker.uri(),
                      address=Address.objects.first(), identification_photo=self.faker.uri())
        self.assertNotIn(pilot, Pilot.objects.all())
        pilot.save()
        self.assertIn(pilot, Pilot.objects.all())
        self.assertEqual(pilot.operator, Operator.objects.first())
        self.assertEqual(pilot.person, Person.objects.first())
        self.assertEqual(pilot.address, Address.objects.first())
        self.assertNotIn(Test.objects.first(), pilot.tests.all())
        pilot.tests.add(Test.objects.first())
        self.assertIn(Test.objects.first(), pilot.tests.all())

    def test_registry_test_validity_create(self):
        test_validity = TestValidity(test=Test.objects.first(), pilot=Pilot.objects.first(), taken_at=timezone.now(),
                                     expiration=timezone.now() + timezone.timedelta(days=365 * 5))

        self.assertNotIn(test_validity, TestValidity.objects.all())
        test_validity.save()
        self.assertIn(test_validity, TestValidity.objects.all())
        self.assertEqual(test_validity.test, Test.objects.first())
        self.assertEqual(test_validity.pilot, Pilot.objects.first())

    def test_registry_type_certificate_create(self):
        type_certificate = TypeCertificate(type_certificate_id=self.faker.numerify('#' * 100),
                                           type_certificate_issuing_country=self.faker.country(),
                                           type_certificate_holder=self.faker.name(),
                                           type_certificate_holder_country=self.faker.country())
        self.assertNotIn(type_certificate, TypeCertificate.objects.all())
        type_certificate.save()
        self.assertIn(type_certificate, TypeCertificate.objects.all())

    def test_registry_manufacturer_create(self):
        manufacturer = Manufacturer(full_name=self.faker.company(), common_name=self.faker.company_suffix(),
                                    address=Address.objects.first(), acronym=self.faker.word(), role=self.faker.word(),
                                    country=self.faker.country_code())
        self.assertNotIn(manufacturer, Manufacturer.objects.all())
        manufacturer.save()
        self.assertIn(manufacturer, Manufacturer.objects.all())

    def test_registry_firmware_create(self):
        firmware = Firmware(binary_file_url=self.faker.uri(), binary_file_hash=self.faker.text(),
                            version=self.faker.pyfloat(min_value=0, max_value=10.00, right_digits=2),
                            manufacturer=Manufacturer.objects.first(), friendly_name=self.faker.name())
        self.assertNotIn(firmware, Firmware.objects.all())
        firmware.save()
        self.assertIn(firmware, Firmware.objects.all())

    def test_registry_aircraft_create(self):
        aircraft = Aircraft(operator=Operator.objects.first(), manufacturer=Manufacturer.objects.first(),
                            name=self.faker.first_name(), flight_controller_id=self.faker.numerify('#' * 60),
                            category=self.faker.pyint(min_value=0, max_value=len(Aircraft.AIRCRAFT_CATEGORY) - 1),
                            status=self.faker.pyint(min_value=0, max_value=len(Aircraft.STATUS_CHOICES) - 1),
                            photo=self.faker.uri())
        self.assertNotIn(aircraft, Aircraft.objects.all())
        aircraft.save()
        self.assertIn(aircraft, Aircraft.objects.all())
        self.assertEqual(aircraft.operator, Operator.objects.first())
        self.assertEqual(aircraft.manufacturer, Manufacturer.objects.first())
        self.assertNotIn(AircraftComponent.objects.first(), aircraft.components.all())
        aircraft.components.add(AircraftComponent.objects.first())
        self.assertIn(AircraftComponent.objects.first(), aircraft.components.all())

    def test_registry_aircraft_detail_create(self):
        aircraft_detail = AircraftDetail(aircraft=Aircraft.objects.first(),
                                         mass=self.faker.pyint(min_value=0, max_value=50),
                                         sub_category=self.faker.pyint(min_value=0, max_value=len(
                                             AircraftDetail.AIRCRAFT_SUB_CATEGORY) - 1),
                                         max_certified_takeoff_weight=self.faker.pyfloat(min_value=0, max_value=50.00,
                                                                                         right_digits=2),
                                         max_height_attainable=self.faker.pyfloat(min_value=0, max_value=160.00,
                                                                                  right_digits=2),
                                         is_registered=True,
                                         max_endurance=self.faker.pyfloat(min_value=0, max_value=20, right_digits=2),
                                         max_range=self.faker.pyfloat(min_value=0, max_value=100.00, right_digits=2),
                                         max_speed=self.faker.pyfloat(min_value=0, max_value=70.00, right_digits=2),
                                         dimension_length=self.faker.pyfloat(min_value=0, max_value=200.00,
                                                                             right_digits=2),
                                         dimension_breadth=self.faker.pyfloat(min_value=0, max_value=200.00,
                                                                              right_digits=2),
                                         dimension_height=self.faker.pyfloat(min_value=0, max_value=20.00,
                                                                             right_digits=2),                                         
                                         icao_aircraft_type_designator=self.faker.numerify('#' * 4),
                                         registration_mark=self.faker.numerify('#' * 10),
                                         commission_date=self.faker.date_time(tzinfo=pytz.UTC),
                                         operating_frequency=self.faker.pyfloat(min_value=0, max_value=500.00,
                                                                                right_digits=2),
                                         manufactured_at=timezone.now(), 
                                         type_certificate=TypeCertificate.objects.first(),
                                         identification_photo=self.faker.uri())

        self.assertNotIn(aircraft_detail, AircraftDetail.objects.all())
        aircraft_detail.save()
        self.assertIn(aircraft_detail, AircraftDetail.objects.all())
        self.assertEqual(aircraft_detail.aircraft, Aircraft.objects.first())
        self.assertEqual(aircraft_detail.type_certificate, TypeCertificate.objects.first())

    def test_registry_aircraft_component_create(self):
        aircraft_component = AircraftComponent(name=self.faker.name(), supplier_part_id=self.faker.numerify('#' * 18), photo=self.faker.uri())
        self.assertNotIn(aircraft_component, AircraftComponent.objects.all())
        aircraft_component.save()
        self.assertIn(aircraft_component, AircraftComponent.objects.all())

    def test_registry_aircraft_component_signature_create(self):
        aircraft_component_signature = AircraftComponentSignature(component=AircraftComponent.objects.first(),
                                                                  signature_url=self.faker.uri())
        self.assertNotIn(aircraft_component_signature, AircraftComponentSignature.objects.all())
        aircraft_component_signature.save()
        self.assertIn(aircraft_component_signature, AircraftComponentSignature.objects.all())
        self.assertEqual(aircraft_component_signature.component, AircraftComponent.objects.first())

    def test_pki_framework_aerobridge_credential_create(self):
        aerobridge_credentials = AerobridgeCredential(name=self.faker.name(),
                                                      token_type=self.faker.pyint(min_value=0, max_value=len(
                                                          AerobridgeCredential.TOKEN_TYPE) - 1),
                                                      association=self.faker.pyint(min_value=0, max_value=len(
                                                          AerobridgeCredential.KEY_ENVIRONMENT) - 1),
                                                      token=self.faker.binary(length=1024), is_active=True)
        self.assertNotIn(aerobridge_credentials, AerobridgeCredential.objects.all())
        aerobridge_credentials.save()
        self.assertIn(aerobridge_credentials, AerobridgeCredential.objects.all())
