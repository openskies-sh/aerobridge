from rest_framework import serializers

from registry.models import Activity, Authorization, Operator, Contact, Aircraft, Pilot, Address, Person, Test, \
    TypeCertificate, Company, TestValidity, AircraftDetail, AircraftComponent, AircraftComponentSignature


class AircraftComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftComponent
        fields = '__all__'

class AircraftComponentSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftComponentSignature
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address_line_1', 'address_line_2', 'address_line_3', 'postcode', 'city', 'country',
                  'created_at', 'updated_at')


class ManufacturerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Company
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
        fields = ('id', 'type_certificate_id', 'type_certificate_issuing_country', 'type_certificate_holder',
                  'type_certificate_holder_country',)


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
        fields = (
            'id', 'company_name', 'country', 'website', 'email', 'operator_type', 'address',
            'operational_authorizations',
            'authorized_activities', 'contacts', 'phone_number', 'company_number', 'country', 'pilots', 'aircrafts',
            'created_at', 'updated_at')


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
    address = AddressSerializer(read_only=True)
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
        fields = ('id', 'operator', 'person', 'photo', 'address', 'is_active','tests',)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class TestsValiditySerializer(serializers.ModelSerializer):
    tests = TestsSerializer(read_only=True, many=True)
    pilot = PilotSerializer(read_only=True)

    class Meta:
        model = TestValidity
        fields = ('id', 'tests', 'pilot', 'taken_at', 'expiration')


class AircraftFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('id', 'operator', 'manufacturer', 'name', 'status',
                  'final_assembly', "photo",
                  "flight_controller_id")


class AircraftDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftDetail
        fields = '__all__'
