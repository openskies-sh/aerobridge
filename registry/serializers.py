from rest_framework import serializers

from digitalsky_provider.models import Transaction
from registry.models import Authorization, Operator, Contact, Aircraft, Pilot, Address, Person, Test, \
    TypeCertificate, Manufacturer, TestValidity


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address_line_1', 'address_line_2', 'address_line_3', 'postcode', 'city', 'country',
                  'created_at', 'updated_at')

class ManufacturerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ('id', 'full_name', 'common_name', 'address', 'role')

class AuthorizationSerializer(serializers.ModelSerializer):
    risk_type = serializers.SerializerMethodField()
    authorization_type = serializers.SerializerMethodField()
    operation_area_type = serializers.SerializerMethodField()

    def get_risk_type(self, obj):
        return obj.get_risk_type_display()

    def get_authorization_type(self, obj):
        return obj.get_authorization_type_display()

    def get_operation_area_type(self, obj):
        return obj.get_operation_area_type_display()

    class Meta:
        model = Authorization
        fields = ('title', 'risk_type', 'authorization_type', 'operation_area_type', 'end_date')


class TypeCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCertificate
        fields = ('id', 'type_certificate_id', 'type_certificate_issuing_country', 'type_certificate_holder','type_certificate_holder_country',)

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'created_at', 'updated_at')

class TestsSerializer(serializers.ModelSerializer):
    test_type = serializers.SerializerMethodField()
    taken_at = serializers.SerializerMethodField()

    def get_test_type(self, obj):
        return obj.get_test_type_display()

    def get_taken_at(self, obj):
        return obj.get_taken_at_display()

    class Meta:
        model = Test
        fields = ('id', 'test_type', 'taken_at', 'created_at', 'updated_at')

class OperatorSerializer(serializers.ModelSerializer):
    ''' This is the default serializer for Operator '''

    class Meta:
        model = Operator
        fields = '__all__'


class PrivilegedOperatorSerializer(serializers.ModelSerializer):
    ''' This is the privileged serializer for Operator specially for law enforcement and other privileged operators '''
    authorized_activities = serializers.SerializerMethodField()
    operational_authorizations = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)

    def get_authorized_activities(self, response):
        activities = []
        o = Operator.objects.get(id=response.id)
        oa = o.authorized_activities.all()
        for activity in oa:
            activities.append(activity.name)
        return activities

    def get_operational_authorizations(self, response):
        authorizations = []
        o = Operator.objects.get(id=response.id)
        oa = o.operational_authorizations.all()
        for authorization in oa:
            authorizations.append(authorization.title)
        return authorizations

    class Meta:
        model = Operator
        fields = ('id', 'company_name', 'country', 'website', 'email', 'operator_type', 'address',
                  'operational_authorizations', 'authorized_activities', 'created_at', 'updated_at')

class OperatorSelectRelatedSerializer(serializers.ModelSerializer):
    ''' This is the privileged serializer for Operator specially for law enforcement and other privileged operators '''
    authorized_activities = serializers.SerializerMethodField()
    operational_authorizations = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)
    pilots = serializers.SerializerMethodField()
    aircrafts = serializers.SerializerMethodField()

    def get_authorized_activities(self, response):
        activities = []
        o = Operator.objects.get(id=response.id)
        oa = o.authorized_activities.all()
        for activity in oa:
            activities.append(activity.name)
        return activities

    def get_operational_authorizations(self, response):
        authorizations = []
        o = Operator.objects.get(id=response.id)
        oa = o.operational_authorizations.all()
        for authorization in oa:
            authorization_serializer = AuthorizationSerializer(authorization)
            authorizations.append(authorization_serializer.data)
        return authorizations

    def get_contacts(self, response):
        all_contacts = []
        o = Operator.objects.get(id=response.id)
        contacts = Contact.objects.filter(operator=o)
        for contact in contacts:
            contact_serializer = PersonSerializer(contact.person)
            address_serializer = AddressSerializer(contact.address)
            contact_data = contact_serializer.data
            address_data = address_serializer.data
            contact_data.update(address_data)

            all_contacts.append(contact_data)
        return all_contacts

    def get_aircrafts(self, response):
        all_aircrafts = []
        o = Operator.objects.get(id=response.id)
        aircrafts = Aircraft.objects.filter(operator=o)
        for aircraft in aircrafts:
            aircraft_serializer = AircraftSerializer(aircraft)
            all_aircrafts.append(aircraft_serializer.data)
        return all_aircrafts

    def get_pilots(self, response):
        all_pilots = []
        o = Operator.objects.get(id=response.id)
        pilots = Pilot.objects.filter(operator=o)
        for pilot in pilots:
            contact_serializer = PersonSerializer(pilot.person)
            address_serializer = AddressSerializer(pilot.address)
            pilot_data = contact_serializer.data
            address_data = address_serializer.data
            pilot_data.update(address_data)
            pilot_data.update({'id': pilot.id})
            all_pilots.append(pilot_data)

        return all_pilots

    class Meta:
        model = Operator
        fields = ('id', 'company_name', 'country', 'website', 'email', 'operator_type', 'address','operational_authorizations', 'authorized_activities', 'contacts', 'phone_number', 'company_number','country', 'pilots', 'aircrafts', 'created_at', 'updated_at')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'person', 'role_type', 'updated_at')


class ContactDetailSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    operator = OperatorSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'operator', 'person', 'role_type', 'updated_at')


class PilotSerializer(serializers.ModelSerializer):
    ''' This is the default serializer for Operator '''
    tests = serializers.SerializerMethodField()

    def get_tests(self, response):
        p = Pilot.objects.get(id=response.id)
        tests_validity = TestValidity.objects.filter(pilot=p)
        all_tests = []
        for cur_test_validity in tests_validity:
            test_serializer = TestsSerializer(cur_test_validity.test)
            all_tests.append({'expiration': cur_test_validity.expiration, 'test_details': test_serializer.data})
        return all_tests

    class Meta:
        model = Pilot
        fields = ('id', 'operator', 'person', 'photo', 'photo_small', 'address', 'identification_photo','identification_photo_small', 'tests')


class TestsValiditySerializer(serializers.ModelSerializer):
    tests = TestsSerializer(read_only=True, many=True)
    pilot = PilotSerializer(read_only=True)

    class Meta:
        model = TestValidity
        fields = ('id', 'tests', 'pilot', 'taken_at', 'expiration')


class PilotDetailSerializer(serializers.ModelSerializer):
    tests = serializers.SerializerMethodField()
    person = PersonSerializer(read_only=True)

    def get_tests(self, response):
        p = Pilot.objects.get(id=response.id)
        tests_validity = TestValidity.objects.filter(pilot=p)
        all_tests = []
        for cur_test_validity in tests_validity:
            test_serializer = TestsSerializer(cur_test_validity.test)
            all_tests.append({'expiration': cur_test_validity.expiration, 'test_details': test_serializer.data})
        return all_tests

    class Meta:
        model = Pilot
        fields = ('id', 'operator', 'person', 'photo', 'photo_small', 'address', 'person', 'is_active',
                  'identification_photo', 'identification_photo_small', 'tests')


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('id', 'operator', 'mass', 'manufacturer', 'model', 'manufacturer', 'status', 'registration_mark',
                  'category', 'created_at', 'popular_name', 'manufacturer', 'registration_mark', 'sub_category',
                  "flight_controller_number", "photo", "photo_small", 'max_certified_takeoff_weight', 'updated_at',
                  'photo_small', 'photo')


class AircraftSigningSerializer(serializers.ModelSerializer):
    droneTypeId = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    deviceId = serializers.SerializerMethodField()
    deviceModelId = serializers.SerializerMethodField()
    operatorBusinessIdentifier = serializers.SerializerMethodField()
    txn = serializers.SerializerMethodField()

    def get_txn(self, response):
        drone = Aircraft.objects.get(id=response.id)
        t, created = Transaction.objects.get_or_create(aircraft_id=drone.id, prefix="tsc_signing")
        return t.id

    def get_droneTypeId(self, response):
        a = Aircraft.objects.get(id=response.id)
        return a.sub_category

    def get_version(self, response):
        a = Aircraft.objects.get(id=response.id)
        return a.model

    def get_deviceId(self, response):
        a = Aircraft.objects.get(id=response.id)
        return a.esn

    def get_deviceModelId(self, response):
        a = Aircraft.objects.get(id=response.id)
        return a.maci_number

    def get_operatorBusinessIdentifier(self, response):
        a = Aircraft.objects.get(id=response.id)
        return a.operator.id

    class Meta:
        model = Aircraft
        fields = ('droneTypeId', 'version', 'deviceId', 'deviceModelId', 'txn', 'operatorBusinessIdentifier')


class AircraftDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        exclude = ('is_registered',)
