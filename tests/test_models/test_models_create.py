from django.utils import timezone

from digitalsky_provider.models import DigitalSkyLog, AircraftRegister
from gcs_operations.models import FlightPlan, FlightOperation, Transaction, FlightPermission, FlightLog, UINApplication
from registry.models import Person, Address, Activity, Authorization, Operator, Contact, Test, TypeCertificate, \
    Manufacturer, Engine, Firmware, Pilot, TestValidity, Aircraft
from .test_setup import TestModels


class TestModelsCreate(TestModels):
    fixtures = ['Activity', 'Address', 'Authorization', 'Engine', 'Manufacturer', 'Operator', 'Person', 'Test',
                'TypeCertificate', 'Pilot', 'FlightPlan', 'FlightOperation', 'Aircraft', 'Transaction']

    def test_digitalsky_provider_digitalsky_log_create(self):
        digitalsky_log = DigitalSkyLog(txn=Transaction.objects.first(), response_code=self.faker.numerify('###'),
                                       response=self.faker.sentence(), timestamp=timezone.now())
        self.assertNotIn(digitalsky_log, DigitalSkyLog.objects.all())
        digitalsky_log.save()
        self.assertIn(digitalsky_log, DigitalSkyLog.objects.all())
        self.assertEqual(digitalsky_log.txn, Transaction.objects.first())

    def test_digitalsky_provider_aircraft_register_create(self):
        aircraft_register = AircraftRegister(is_signed=True, drone=Aircraft.objects.first(),
                                             signature=self.faker.text(), certificate=self.faker.text())
        self.assertNotIn(aircraft_register, AircraftRegister.objects.all())
        aircraft_register.save()
        self.assertIn(aircraft_register, AircraftRegister.objects.all())
        self.assertEqual(aircraft_register.drone, Aircraft.objects.first())

    def test_gcs_operations_flight_plan_create(self):
        flight_plan = FlightPlan(name=self.faker.word(), geo_json=self.faker.sentence(), start_datetime=timezone.now(),
                                 end_datetime=timezone.now() + timezone.timedelta(minutes=30))
        self.assertNotIn(flight_plan, FlightPlan.objects.all())
        flight_plan.save()
        self.assertIn(flight_plan, FlightPlan.objects.all())

    def test_gcs_operations_flight_operation_create(self):
        flight_operation = FlightOperation(name=self.faker.word(), drone=Aircraft.objects.first(),
                                           flight_plan=FlightPlan.objects.first(), purpose=Activity.objects.first(),
                                           type_of_operation=self.faker.pyint(min_value=0, max_value=len(
                                               FlightOperation.OPERATION_TYPES) - 1),
                                           flight_termination_or_return_home_capability=True,
                                           geo_fencing_capability=True, detect_and_avoid_capability=True)
        self.assertNotIn(flight_operation, FlightOperation.objects.all())
        flight_operation.save()
        self.assertIn(flight_operation, FlightOperation.objects.all())
        self.assertEqual(flight_operation.drone, Aircraft.objects.first())
        self.assertEqual(flight_operation.flight_plan, FlightPlan.objects.first())
        self.assertEqual(flight_operation.purpose, Activity.objects.first())

    def test_gcs_operations_transaction_create(self):
        transaction = Transaction(prefix=self.faker.word(), aircraft=Aircraft.objects.first())
        self.assertNotIn(transaction, Transaction.objects.all())
        transaction.save()
        self.assertIn(transaction, Transaction.objects.all())
        self.assertEqual(transaction.aircraft, Aircraft.objects.first())

    def test_gcs_operations_flight_permission_create(self):
        flight_permission = FlightPermission(operation=FlightOperation.objects.first(), is_successful=True,
                                             artefact=self.faker.text())
        self.assertNotIn(flight_permission, FlightPermission.objects.all())
        flight_permission.save()
        self.assertIn(flight_permission, FlightPermission.objects.all())
        self.assertEqual(flight_permission.operation, FlightOperation.objects.first())

    def test_gcs_operations_flight_log_create(self):
        flight_log = FlightLog(operation=FlightOperation.objects.first(), signed_log=self.faker.uri_path(),
                               raw_log=self.faker.uri_path(), is_submitted=True)
        self.assertNotIn(flight_log, FlightLog.objects.all())
        flight_log.save()
        self.assertIn(flight_log, FlightLog.objects.all())
        self.assertEqual(flight_log.operation, FlightOperation.objects.first())

    def test_gcs_operations_uin_application_create(self):
        uin_application = UINApplication(fee_details=self.faker.word(), drone=Aircraft.objects.first(),
                                         operator=Operator.objects.first(), import_permission=self.faker.uri(),
                                         cin=self.faker.uri(), gst_in=self.faker.uri(), pan_card=self.faker.uri(),
                                         dot_permission=self.faker.uri(), security_clearance=self.faker.uri(),
                                         eta=self.faker.uri(), op_manual=self.faker.uri(),
                                         maintainence_guidelines=self.faker.uri(),
                                         counter=self.faker.pyint(min_value=0, max_value=50))
        self.assertNotIn(uin_application, UINApplication.objects.all())
        uin_application.save()
        self.assertIn(uin_application, UINApplication.objects.all())
        self.assertEqual(uin_application.operator, Operator.objects.first())
        self.assertEqual(uin_application.drone, Aircraft.objects.first())

    def test_registry_person_create(self):
        person = Person(first_name=self.faker.first_name(), last_name=self.faker.last_name(), email=self.faker.email(),
                        phone_number=self.faker.numerify('+' + '#' * 9),
                        identification_number=self.faker.numerify('#' * 15),
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
        operator = Operator(company_name=self.faker.company(), website=self.faker.url(), email=self.faker.company_email,
                            phone_number=self.faker.numerify('+' + '#' * 9),
                            operator_type=self.faker.pyint(min_value=0, max_value=len(
                                Operator.OPTYPE_CHOICES) - 1), address=Address.objects.first(),
                            vat_number=self.faker.numerify('+' + '#' * 24),
                            insurance_number=self.faker.numerify('+' + '#' * 24), country='IN')
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
                      photo_small=self.faker.uri(), address=Address.objects.first(),
                      identification_photo=self.faker.uri(), identification_photo_small=self.faker.uri())
        self.assertNotIn(pilot, Pilot.objects.all())
        pilot.save()
        self.assertIn(pilot, Pilot.objects.all())
        self.assertEqual(pilot.operator, Operator.objects.first())
        self.assertEqual(pilot.person, Person.objects.first())
        self.assertEqual(pilot.address, Address.objects.first())
        self.assertNotIn(Test.objects.first(), pilot.tests.all())
        pilot.tests.add(Test.objects.first())
        self.assertIn(Test.objects.first(), pilot.tests.all())

    def test_registry_testValidity_create(self):
        test_validity = TestValidity(test=Test.objects.first(), pilot=Pilot.objects.first(), taken_at=timezone.now(),
                                     expiration=timezone.now() + timezone.timedelta(days=365 * 5))

        self.assertNotIn(test_validity, TestValidity.objects.all())
        test_validity.save()
        self.assertIn(test_validity, TestValidity.objects.all())
        self.assertEqual(test_validity.test, Test.objects.first())
        self.assertEqual(test_validity.pilot, Pilot.objects.first())

    def test_registry_typeCertificate_create(self):
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
                                    country=self.faker.country_code(), digital_sky_id=self.faker.numerify('#' * 20))
        self.assertNotIn(manufacturer, Manufacturer.objects.all())
        manufacturer.save()
        self.assertIn(manufacturer, Manufacturer.objects.all())

    def test_registry_engine_create(self):
        engine = Engine(type=self.faker.word(), power=self.faker.pyfloat(min_value=0, max_value=100.00, right_digits=2),
                        count=self.faker.pyint(min_value=0, max_value=50), engine_type=self.faker.word(),
                        propellor=self.faker.sentence())
        self.assertNotIn(engine, Engine.objects.all())
        engine.save()
        self.assertIn(engine, Engine.objects.all())

    def test_registry_firmware_create(self):
        firmware = Firmware(binary_file_url=self.faker.uri(), public_key=self.faker.text(),
                            version=self.faker.pyfloat(min_value=0, max_value=10.00, right_digits=2),
                            manufacturer=Manufacturer.objects.first())
        self.assertNotIn(firmware, Firmware.objects.all())
        firmware.save()
        self.assertIn(firmware, Firmware.objects.all())

    def test_registry_aircraft_create(self):
        aircraft = Aircraft(operator=Operator.objects.first(), mass=self.faker.pyint(min_value=0, max_value=50),
                            is_airworthy=True, make=self.faker.sentence(), master_series=self.faker.sentence(),
                            series=self.faker.sentence(), popular_name=self.faker.word(),
                            manufacturer=Manufacturer.objects.first(),
                            category=self.faker.pyint(min_value=0, max_value=len(Aircraft.AIRCRAFT_CATEGORY) - 1),
                            registration_mark=self.faker.numerify('#' * 10),
                            sub_category=self.faker.pyint(min_value=0, max_value=len(
                                Aircraft.AIRCRAFT_SUB_CATEGORY) - 1),
                            icao_aircraft_type_designator=self.faker.numerify('#' * 4),
                            max_certified_takeoff_weight=self.faker.pyfloat(min_value=0, max_value=50.00,
                                                                            right_digits=2),
                            max_height_attainable=self.faker.pyfloat(min_value=0, max_value=160.00, right_digits=2),
                            compatible_payload=self.faker.text(max_nb_chars=20), commission_date=timezone.now(),
                            type_certificate=TypeCertificate.objects.first(), model=self.faker.text(),
                            esn=self.faker.numerify('#' * 20), digital_sky_uin_number=self.faker.numerify('#' * 30),
                            maci_number=self.faker.mac_address(),
                            flight_controller_number=self.faker.numerify('#' * 60),
                            controller_public_key=self.faker.text(),
                            operating_frequency=self.faker.pyfloat(min_value=0, max_value=500.00, right_digits=2),
                            status=self.faker.pyint(min_value=0, max_value=len(Aircraft.STATUS_CHOICES) - 1),
                            photo=self.faker.uri(), photo_small=self.faker.uri(), identification_photo=self.faker.uri(),
                            identification_photo_small=self.faker.uri(), engine=Engine.objects.first(),
                            is_registered=True,
                            fuel_capacity=self.faker.pyfloat(min_value=0, max_value=50, right_digits=1),
                            max_endurance=self.faker.pyfloat(min_value=0, max_value=20, right_digits=2),
                            max_range=self.faker.pyfloat(min_value=0, max_value=100.00, right_digits=2),
                            max_speed=self.faker.pyfloat(min_value=0, max_value=70.00, right_digits=2),
                            dimension_length=self.faker.pyfloat(min_value=0, max_value=200.00, right_digits=2),
                            dimension_breadth=self.faker.pyfloat(min_value=0, max_value=200.00, right_digits=2),
                            dimension_height=self.faker.pyfloat(min_value=0, max_value=20.00, right_digits=2),
                            manufactured_at=timezone.now(), dot_permission_document=self.faker.uri(),
                            operataions_manual_document=self.faker.uri()
                            )
        self.assertNotIn(aircraft, Aircraft.objects.all())
        aircraft.save()
        self.assertIn(aircraft, Aircraft.objects.all())
        self.assertEqual(aircraft.operator, Operator.objects.first())
        self.assertEqual(aircraft.manufacturer, Manufacturer.objects.first())
        self.assertEqual(aircraft.type_certificate, TypeCertificate.objects.first())
        self.assertEqual(aircraft.engine, Engine.objects.first())
