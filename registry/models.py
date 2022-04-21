from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from . import countries
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from common.settings import currency_code_default as cc_default
from common.validators import validate_currency_code
from django.db.models import Sum, Q
from moneyed import CURRENCIES
# Source https://stackoverflow.com/questions/63830942/how-do-i-validate-if-a-django-urlfield-is-from-a-specific-domain-or-hostname

def validate_flight_controller_id(value):
    if not value.isalnum():
        raise ValidationError(u'%s flight controller ID cannot contain special characters or spaces' % value)


def validate_url(value):
    if not value:
        return  # Required error is done the field
    parsed_url = urlparse(value)
    if not bool(parsed_url.scheme):
        raise ValidationError('Only valid urls are allowed')


def two_year_expiration():
    return datetime.combine(date.today() + relativedelta(months=+24), datetime.min.time()).replace(tzinfo=timezone.utc)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$',
                                             message="No special characters allowed in this field.")

class AerobridgeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(help_text="Give a name for this document")
    url = models.URLField(blank=True, null=True, validators=[validate_url,],
                                              default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, help_text="The first name of the person added to the database")
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(help_text="Associate a email address with the person, this field is required")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    help_text="Associate a phone number with this person")

    documents = models.ManyToManyField(AerobridgeDocument)   
    social_security_number = models.CharField(max_length=25, blank=True, null=True,
                                              help_text="If social security / identification number is avaialble associate it with a person")
                                
    date_of_birth = models.DateField(blank=True, null=True, help_text="Assign a date of birth with this person")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Address(models.Model):
    STATE_CHOICES = (
    ("AN", _("Andaman and Nicobar Islands")), ("AP", _("Andhra Pradesh")), ("AR", _("Arunachal Pradesh")),
    ("AS", _("Assam")), ("BR", _("Bihar")), ("CG", _("Chandigarh")), ("CH", _("Chhattisgarh")),
    ("DN", _("Dadra and Nagar Haveli")), ("DD", _("Daman and Diu")), ("DL", _("Delhi")), ("GA", _("Goa")),
    ("GJ", _("Gujarat")), ("HR", _("Haryana")), ("HP", _("Himachal Pradesh")), ("JK", _("Jammu and Kashmir")),
    ("JH", _("Jharkhand")), ("KA", _("Karnataka")), ("KL", _("Kerala")), ("LA", _("Ladakh")), ("LD", _("Lakshadweep")),
    ("MP", _("Madhya Pradesh")), ("MH", _("Maharashtra")), ("MN", _("Manipur")), ("ML", _("Meghalaya")),
    ("MZ", _("Mizoram")), ("NL", _("Nagaland")), ("OR", _("Odisha")), ("PY", _("Puducherry")), ("PB", _("Punjab")),
    ("RJ", _("Rajasthan")), ("SK", _("Sikkim")), ("TN", _("Tamil Nadu")), ("TS", _("Telangana")), ("TR", _("Tripura")),
    ("UP", _("Uttar Pradesh")), ("UK", _("Uttarakhand")), ("WB", _("West Bengal")))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_1 = models.CharField(max_length=140)
    address_line_2 = models.CharField(max_length=140, blank=True, null=True)
    address_line_3 = models.CharField(max_length=140, blank=True, null=True)
    postcode = models.CharField(_("post code"), max_length=10)
    city = models.CharField(max_length=140, help_text="Set a city for this address")
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATE_CHOICES,
                             help_text="Pick a state, at the moment only Indian States are configured.")
    country = models.CharField(max_length=2, choices=countries.COUNTRY_CHOICES_ISO3166, default='IN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.address_line_1 + ', ' + self.city + ' ' + self.country

    def __str__(self):
        return self.address_line_1 + ', ' + self.city + ' ' + self.country

    # Create your models here.


class Activity(models.Model):
    ACTIVITYTYPE_CHOICES = ((0, _('NA')), (1, _('Open')), (2, _('Specific')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, help_text="Set a name for this activity")
    activity_type = models.IntegerField(choices=ACTIVITYTYPE_CHOICES, default=0,
                                        help_text="Set the activity type and the airspace")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Authorization(models.Model):
    AREATYPE_CHOICES = ((0, _('Unpopulated')), (1, _('Sparsely Populated')), (2, _('Densely Populated')),)
    RISKCLASS_CHOICES = (
    (0, _('NA')), (1, _('SAIL 1')), (2, _('SAIL 2')), (3, _('SAIL 3')), (4, _('SAIL 4')), (5, _('SAIL 5')),
    (6, _('SAIL 6')),)
    AUTHTYPE_CHOICES = (
    (0, _('NA')), (1, _('Light UAS Operator Certificate')), (2, _('Standard Scenario Authorization')),)
    AIRSPACE_CHOICES = ((0, _('NA')), (1, _('Green')), (2, _('Amber')), (3, _('Red')),)
    ALTITUDE_SYSTEM = ((0, _('wgs84')), (1, _('amsl')), (2, _('agl')), (3, _('sps')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=140)
    operation_max_height = models.IntegerField(default=0,
                                               help_text="Set the maximum authorized height for this authorization")
    operation_altitude_system = models.IntegerField(default=0, choices=ALTITUDE_SYSTEM,
                                                    help_text="Set the altitude system")
    airspace_type = models.IntegerField(choices=AIRSPACE_CHOICES, default=0,
                                        help_text="Set the airspace type, if available")
    permit_to_fly_above_crowd = models.BooleanField(default=0,
                                                    help_text="Select if the company is permitted to fly above crowd")
    operation_area_type = models.IntegerField(choices=AREATYPE_CHOICES, default=0,
                                              help_text="Can the operator fly over crowds? ")
    risk_type = models.IntegerField(choices=RISKCLASS_CHOICES, default=0,
                                    help_text="If available, set the airspace risk type")
    authorization_type = models.IntegerField(choices=AUTHTYPE_CHOICES, default=0,
                                             help_text="Set the type of the authorization")
    end_date = models.DateTimeField(default=two_year_expiration,
                                    help_text="By default every authorization exipres in two years, you can set a different end date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Operator(models.Model):
    OPTYPE_CHOICES = ((0, _('NA')), (1, _('LUC')), (2, _('Non-LUC')), (3, _('AUTH')), (4, _('DEC')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expiration = models.DateTimeField(default=two_year_expiration)
    operator_type = models.IntegerField(choices=OPTYPE_CHOICES, default=0,
                                        help_text="Choose what kind of operator this is, classify the operator based on capabilites, use the adminsitration panel to add additional operator categories")
                                        
    operational_authorizations = models.ManyToManyField(Authorization, related_name='operational_authorizations',
                                                        help_text="Choose what kind of authorization this operator posseses, to add additional authorizations, use the administration panel")
    authorized_activities = models.ManyToManyField(Activity, related_name='authorized_activities',
                                                   help_text="Related to Authorization, select the kind of activities that this operator is allowed to conduct, you can add additional activities using the administration panel")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_address(self):
        full_address = '%s, %s, %s, %s %s, %s' % (
        self.address.address_line_1, self.address.address_line_2, self.address.address_line_3, self.address.city,
        self.address.state, self.address.country)
        return full_address

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    ROLE_CHOICES = ((0, _('Other')), (1, _('Responsible')))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, related_name='person_contact',
                                 help_text="Set a operator for this contact")
    person = models.ForeignKey(Person, models.CASCADE, help_text="Associate a person for this contact")
    address = models.ForeignKey(Address, models.CASCADE, help_text="Add a address for this contact")
    role_type = models.IntegerField(choices=ROLE_CHOICES, default=0,
                                    help_text="A contact may or may not be legally responsible officer within a company, specify if the contact is responsisble (legally) for operations in the company")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company_name

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company_name


class Test(models.Model):
    TESTTYPE_CHOICES = (
    (0, _('Remote pilot online theoretical competency')), (1, _('Certificate of remote pilot competency')),
    (2, _('Other')),)
    TAKEN_AT_CHOICES = ((0, _('Online Test')), (1, _('In Authorized Test Center')), (2, _('Other')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_type = models.IntegerField(choices=TESTTYPE_CHOICES, default=0, help_text="Specify the type of test")
    taken_at = models.IntegerField(choices=TAKEN_AT_CHOICES, default=0, help_text="Specify where this test was taken")
    name = models.CharField(max_length=100, help_text="Set a name for this test that can be understood")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Pilot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Assign this pilot to a operator")
    person = models.OneToOneField(Person, models.CASCADE,
                                  help_text="Assign this pilot to a person object in the database")
    photo = models.URLField(blank=True, null=True, validators=[validate_url, ],
                            help_text="A URL to link to a photo of the pilot")

    address = models.ForeignKey(Address, models.CASCADE, help_text="Assign a address to this Pilot")
    
    documents = models.ManyToManyField(AerobridgeDocument)   
                                
    tests = models.ManyToManyField(Test, through='TestValidity',
                                   help_text="Specify the tests if any the pilot has taken")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=0,
                                    help_text="Is this pilot active? If he is not working for the company or has moved on, set it as inactive")

    def __unicode__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company_name

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company_name


class TestValidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, models.CASCADE)
    pilot = models.ForeignKey(Pilot, models.CASCADE)
    taken_at = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)


class TypeCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_certificate_id = models.CharField(max_length=280)
    type_certificate_issuing_country = models.CharField(max_length=280)
    type_certificate_holder = models.CharField(max_length=140)
    type_certificate_holder_country = models.CharField(max_length=140)

    def __unicode__(self):
        return self.type_certificate_holder

    def __str__(self):
        return self.type_certificate_holder


class Company(models.Model):

    COMPANY_TYPE = (
    (0, _('Supplier')), (1, _('Manufacturer')), (2, _('Operator')), (3, _('Customer')),)

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=140, help_text="Full legal name of the manufacturing entity")
    common_name = models.CharField(max_length=140, help_text="Common name for the manufacturer e.g. Skydio")
    address = models.ForeignKey(Address, models.CASCADE, blank=True, null=True,
                                help_text="Assign a address to this manufacturers")
    acronym = models.CharField(max_length=10,
                               help_text="If you use a acronym for this manufacturer, you can assign it here")    
    country = models.CharField(max_length=3,
                               help_text="The three-letter ISO 3166-1 country code where the manufacturer is located")
    website = models.URLField(
        help_text="Put official URL of the company, if none is available then a manufacturers public facing URL is necessary")
    email = models.EmailField(help_text="Contact email for support and other queries")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  #                           
    documents = models.ManyToManyField(AerobridgeDocument, help_text = "You can upload and associate documents to the manufacturer")   
    vat_number = models.CharField(max_length=25, default="VAT-TMP", validators=[no_special_characters_regex, ],
                                  blank=True, null=True, help_text="VAT / Tax number if available")
    insurance_number = models.CharField(max_length=25, default="INS-TMP", validators=[no_special_characters_regex, ],
                                        blank=True, null=True, help_text="Insurance number if avaialble")
    company_number = models.CharField(max_length=25, default='CO-TMP', validators=[no_special_characters_regex, ],
                                      blank=True, null=True, help_text="Company number if available ")
    country = models.CharField(max_length=2, choices=countries.COUNTRY_CHOICES_ISO3166, default='IN',
                               help_text="At the moment only India is configured, you can setup your own country")

    currency = models.CharField(
        max_length=3,
        verbose_name=_('Currency'),
        blank=True,
        default=cc_default,
        help_text=_('Default currency used for this company'),
        validators=[validate_currency_code],
    )

    role = models.IntegerField(choices=COMPANY_TYPE, default=3,
                                 help_text="Set the type of the company")
    @property
    def currency_code(self):
        """
        Return the currency code associated with this company.
        - If the currency code is invalid, use the default currency
        - If the currency code is not specified, use the default currency
        """

        code = self.currency

        if code not in CURRENCIES:
            code = cc_default()

        return code


    @property
    def manufactured_part_count(self):
        """ The number of parts manufactured by this company """
        return self.manufactured_parts.count()

    @property
    def has_manufactured_parts(self):
        return self.manufactured_part_count > 0

    @property
    def supplied_part_count(self):
        """ The number of parts supplied by this company """
        return self.supplied_parts.count()

    @property
    def has_supplied_parts(self):
        """ Return True if this company supplies any parts """
        return self.supplied_part_count > 0

    @property
    def parts(self):
        """ Return SupplierPart objects which are supplied or manufactured by this company """
        return AircraftComponent.objects.filter(Q(supplier=self.id) | Q(manufacturer_part__manufacturer=self.id))

    @property
    def part_count(self):
        """ The number of parts manufactured (or supplied) by this Company """
        return self.parts.count()

    @property
    def has_parts(self):
        return self.part_count > 0

    @property
    def stock_items(self):
        """ Return a list of all stock items supplied or manufactured by this company """
        
        return AircraftComponentStock.objects.filter(Q(supplier_part__supplier=self.id) | Q(supplier_part__manufacturer_part__manufacturer=self.id)).all()

    @property
    def stock_count(self):
        """ Return the number of stock items supplied or manufactured by this company """
        return self.stock_items.count()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.common_name

    def __str__(self):
        return self.common_name


class Firmware(models.Model):
    ''' A model for custom firmware '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    binary_file_url = models.URLField(help_text="Enter a url from where the firmware can be downloaded")
    binary_file_hash = models.TextField(help_text="Enter a SHA / Digest for the firmware, used to secure the firmware")
    version = models.CharField(max_length=25, help_text="Set a semantic version for the firmware version")
    manufacturer = models.ForeignKey(Company, models.CASCADE, help_text="Associate a manufacturer to the firmware", limit_choices_to={'role':1})
    friendly_name = models.CharField(max_length=140, help_text="Give it a friendly name e.g. May-2021 1.2 release")
    is_active = models.BooleanField(default=False,
                                    help_text="Set if the firmware is active, don't forget to mark old firmware as inactive")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.version

    def __str__(self):
        return self.version


# class SupplierPart(models.Model):
#     '''Source: https://github.com/inventree/InvenTree/blob/8a82f22378c2a138a21ed0099e2a48b0d2c48d49/InvenTree/company/models.py#L450''''
#     pass

# class AerobridgeComponentStock(models.Model):
#     pass


class AircraftMasterComponent(models.Model):
    ''' '''

    COMPONENT_TYPE = (
    (0, _('Frame')), (1, _('Motors')), (2, _('Electronic Speed Controller')), (3, _('Flight Controller')),
    (4, _('Power Distribution Board')), (5, _('Battery')), (6, _('Propellors')), (7, _('Camera')), (8, _('GPS')),
    (9, _('Battery Charger')), (10, _('Telemetry Link')), (11, _('Remote Controller')), (12, _('Landing Gear')),
    (13, _('GPS')), (14, _('Companion Computer')),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=280)
    family = models.IntegerField(choices=COMPONENT_TYPE, default=1,
                                 help_text="Set the component family")
    drawing = models.URLField(blank=True, null=True, help_text="A URL to a photo of the component drawing.")

    manufacturer = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name='manufactured_parts',
        limit_choices_to={
            'is_manufacturer': True
        },
        verbose_name=_('Manufacturer'),
        help_text=_('Select manufacturer'),
    )

    MPN = models.CharField(
        null=True,
        max_length=100,
        verbose_name=_('MPN'),
        help_text=_('Manufacturer Part Number')
    )

    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_default_supplier(self):
        """ Get the default supplier part for this part (may be None).
        - If the part specifies a default_supplier, return that
        - If there is only one supplier part available, return that
        - Else, return None
        """

        if self.default_supplier:
            return self.default_supplier

        if self.supplier_count == 1:
            return self.supplier_parts.first()

        # Default to None if there are multiple suppliers to choose from
        return None

    default_supplier = models.ForeignKey(
        SupplierPart,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Default Supplier'),
        help_text=_('Default supplier part'),
        related_name='default_parts'
    )

    default_expiry = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Default Expiry'),
        help_text=_('Expiry time (in days) for stock items of this part'),
    )

    minimum_stock = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)],
        verbose_name=_('Minimum Stock'),
        help_text=_('Minimum allowed stock level')
    )

    units = models.CharField(
        max_length=20, default="",
        blank=True, null=True,
        verbose_name=_('Units'),
        help_text=_('Stock keeping units for this part')
    )

    assembly = models.BooleanField(
        default=part_settings.part_assembly_default,
        verbose_name=_('Assembly'),
        help_text=_('Can this part be built from other parts?')
    )

    component = models.BooleanField(
        default=part_settings.part_component_default,
        verbose_name=_('Component'),
        help_text=_('Can this part be used to build other parts?')
    )

    trackable = models.BooleanField(
        default=part_settings.part_trackable_default,
        verbose_name=_('Trackable'),
        help_text=_('Does this part have tracking for unique items?'))

    purchaseable = models.BooleanField(
        default=part_settings.part_purchaseable_default,
        verbose_name=_('Purchaseable'),
        help_text=_('Can this part be purchased from external suppliers?'))

    salable = models.BooleanField(
        default=part_settings.part_salable_default,
        verbose_name=_('Salable'),
        help_text=_("Can this part be sold to customers?"))

    active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Is this part active?'))

    virtual = models.BooleanField(
        default=part_settings.part_virtual_default,
        verbose_name=_('Virtual'),
        help_text=_('Is this a virtual part, such as a software product or license?'))

    def get_parts_in_bom(self):
        """
        Return a list of all parts in the BOM for this part.
        Takes into account substitutes, variant parts, and inherited BOM items
        """

        parts = set()

        for bom_item in self.get_bom_items():
            for part in bom_item.get_valid_parts_for_allocation():
                parts.add(part)

        return parts

    def check_if_part_in_bom(self, other_part):
        """
        Check if the other_part is in the BOM for this part.
        Note:
            - Accounts for substitute parts
            - Accounts for variant BOMs
        """

        for bom_item in self.get_bom_items():
            if other_part in bom_item.get_valid_parts_for_allocation():
                return True

        # No matches found
        return False

    def check_add_to_bom(self, parent, raise_error=False, recursive=True):
        """
        Check if this Part can be added to the BOM of another part.
        This will fail if:
        a) The parent part is the same as this one
        b) The parent part is used in the BOM for *this* part
        c) The parent part is used in the BOM for any child parts under this one
        """

        result = True

        try:
            if self.pk == parent.pk:
                raise ValidationError({'sub_part': _("Part '{p1}' is  used in BOM for '{p2}' (recursive)").format(
                    p1=str(self),
                    p2=str(parent)
                )})

            bom_items = self.get_bom_items()

            # Ensure that the parent part does not appear under any child BOM item!
            for item in bom_items.all():

                # Check for simple match
                if item.sub_part == parent:
                    raise ValidationError({'sub_part': _("Part '{p1}' is  used in BOM for '{p2}' (recursive)").format(
                        p1=str(parent),
                        p2=str(self)
                    )})

                # And recursively check too
                if recursive:
                    result = result and item.sub_part.check_add_to_bom(
                        parent,
                        recursive=True,
                        raise_error=raise_error
                    )

        except ValidationError as e:
            if raise_error:
                raise e
            else:
                return False

        return result

    @property
    def available_stock(self):
        """
        Return the total available stock.
        - This subtracts stock which is already allocated to builds
        """

        total = self.total_stock
        total -= self.allocation_count()

        return max(total, 0)

    def required_sales_order_quantity(self):
        """
        Return the quantity of this part required for active sales orders
        """

        # Get a list of line items for open orders which match this part
        open_lines = OrderModels.SalesOrderLineItem.objects.filter(
            order__status__in=SalesOrderStatus.OPEN,
            part=self
        )

        quantity = 0

        for line in open_lines:
            # Determine the quantity "remaining" to be shipped out
            remaining = max(line.quantity - line.shipped, 0)
            quantity += remaining

        return quantity

    def required_order_quantity(self):
        """
        Return total required to fulfil orders
        """

        return self.required_build_order_quantity() + self.required_sales_order_quantity()

    @property
    def quantity_to_order(self):
        """
        Return the quantity needing to be ordered for this part.
        Here, an "order" could be one of:
        - Build Order
        - Sales Order
        To work out how many we need to order:
        Stock on hand = self.total_stock
        Required for orders = self.required_order_quantity()
        Currently on order = self.on_order
        Currently building = self.quantity_being_built
        """

        # Total requirement
        required = self.required_order_quantity()

        # Subtract stock levels
        required -= max(self.total_stock, self.minimum_stock)

        # Subtract quantity on order
        required -= self.on_order

        # Subtract quantity being built
        required -= self.quantity_being_built

        return max(required, 0)

    @property
    def net_stock(self):
        """ Return the 'net' stock. It takes into account:
        - Stock on hand (total_stock)
        - Stock on order (on_order)
        - Stock allocated (allocation_count)
        This number (unlike 'available_stock') can be negative.
        """

        return self.total_stock - self.allocation_count() + self.on_order


    def need_to_restock(self):
        """ Return True if this part needs to be restocked
        (either by purchasing or building).
        If the allocated_stock exceeds the total_stock,
        then we need to restock.
        """

        return (self.total_stock + self.on_order - self.allocation_count) < self.minimum_stock

    @property
    def can_build(self):
        """ Return the number of units that can be build with available stock
        """

        # If this part does NOT have a BOM, result is simply the currently available stock
        if not self.has_bom:
            return 0

        total = None

        bom_items = self.get_bom_items().prefetch_related('sub_part__stock_items')

        # Calculate the minimum number of parts that can be built using each sub-part
        for item in bom_items.all():
            stock = item.sub_part.available_stock

            # If (by some chance) we get here but the BOM item quantity is invalid,
            # ignore!
            if item.quantity <= 0:
                continue

            n = int(stock / item.quantity)

            if total is None or n < total:
                total = n

        if total is None:
            total = 0

        return max(total, 0)

    @property
    def active_builds(self):
        """ Return a list of outstanding builds.
        Builds marked as 'complete' or 'cancelled' are ignored
        """

        return self.builds.filter(status__in=BuildStatus.ACTIVE_CODES)

    @property
    def inactive_builds(self):
        """ Return a list of inactive builds
        """

        return self.builds.exclude(status__in=BuildStatus.ACTIVE_CODES)

    @property
    def quantity_being_built(self):
        """
        Return the current number of parts currently being built.
        Note: This is the total quantity of Build orders, *not* the number of build outputs.
              In this fashion, it is the "projected" quantity of builds
        """

        builds = self.active_builds

        quantity = 0

        for build in builds:
            # The remaining items in the build
            quantity += build.remaining

        return quantity

    @property
    def total_stock(self):
        """ Return the total stock quantity for this part.
        - Part may be stored in multiple locations
        - If this part is a "template" (variants exist) then these are counted too
        """

        return self.get_stock_count(include_variants=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class AircraftModel(models.Model):
    ''' This is the primary bill of materials for a aircraft '''
    AIRCRAFT_CATEGORY = (
    (0, _('Other')), (1, _('FIXED WING')), (2, _('ROTORCRAFT')), (3, _('LIGHTER-THAN-AIR')), (4, _('HYBRID LIFT')),
    (5, _('MICRO')), (6, _('SMALL')), (7, _('MEIDUM')), (8, _('Large')),)
    
    AIRCRAFT_SUB_CATEGORY = (
    (0, _('Other')), (1, _('AIRPLANE')), (2, _('NONPOWERED GLIDER')), (3, _('POWERED GLIDER')), (4, _('HELICOPTER')),
    (5, _('GYROPLANE')), (6, _('BALLOON')), (7, _('AIRSHIP')), (8, _('UAV')), (9, _('Multirotor')), (10, _('Hybrid')),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=280, help_text="Give this a name e.g. Aerobridge F1")
    popular_name = models.CharField(max_length=140, help_text="e.g. F1")
    category = models.IntegerField(choices=AIRCRAFT_CATEGORY, default=0,
                                   help_text="Set the category for this aircraft, use the closest aircraft type")
    master_components = models.ManyToManyField(AircraftMasterComponent, name="master_components")   
    series = models.CharField(max_length=10, default="2022.1", help_text="Define the production series for this Aircraft Model e.g. 2022.1") 
    max_endurance = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                        help_text="Set the endurance in minutes")
    max_range = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                    help_text="Set the range in kms for the drone")
    max_speed = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                    help_text="Set the maximum speed in km/hr.")
    dimension_length = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                           help_text="Set the length of the drone in cms")
    dimension_breadth = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                            help_text="Set the breadth of the drone in cms")
    dimension_height = models.DecimalField(decimal_places=2, max_digits=10, default=0.00,
                                           help_text="Set the height of the drone in cms")
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE, help_text="Associate a firmware with this aircraft model")

    
    mass = models.IntegerField(default=300, help_text="Set the vehicle's mass in gms.")
    sub_category = models.IntegerField(choices=AIRCRAFT_SUB_CATEGORY, default=7, help_text='')
    operating_frequency = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)    
    documents = models.ManyToManyField(AerobridgeDocument, help_text="Associate any existing documents to this series / model ")                                                                   
    type_certificate = models.ForeignKey(TypeCertificate, models.CASCADE, blank=True, null=True,
                                         help_text="Set the type certificate if available for the drone")

    max_certified_takeoff_weight = models.DecimalField(decimal_places=3, max_digits=10, default=0.00,
                                                       help_text="Set the takeoff weight for the aircraft in gms.")
    max_height_attainable = models.DecimalField(decimal_places=3, max_digits=10, default=0.00,
                                                help_text="Set the max attainable height in meters")
    icao_aircraft_type_designator = models.CharField(blank=True, null=True, max_length=4, default='0000',
                                                     help_text="If available you can specify the type designator, see https://www.icao.int/publications/doc8643/pages/search.aspx")                                                
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name + ' ' + str(self.series)

    def __str__(self):
        return self.name + ' : Series ' + str(self.series)


class AircraftComponent(models.Model):
    ''' This class stores details of components for an aircraft '''

    CUSTODY_STATUS = ((0, _('Created')), (1, _('Ordered')), (2, _('In Transit')), (3, _('Received')),(4, _('Installed'),),(5, _('Discarded / Removed'),))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_part_id = models.CharField(max_length=280,
                                        help_text="The part ID provided by the supplier / contract manufacturer")
    
    master_component = models.ForeignKey(AircraftMasterComponent, on_delete=models.CASCADE, help_text="Set the master component associated with this component")
    custody_on = models.DateTimeField(blank=True, null=True,
                                      help_text="Enter a date when this component was in custody of the manufacturer")
    is_active = models.BooleanField(default=True)

    custody_status = models.IntegerField(choices=CUSTODY_STATUS, default=0,
                                 help_text="Set the component status as it moves through the supply chain")
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.master_component.name + ' ' + self.supplier_part_id

    def __str__(self):
        return self.master_component.name + ' ' + self.supplier_part_id


class AircraftComponentSignature(models.Model):
    ''' This model saves information about the component signature on a the block chain '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(AircraftComponent, on_delete=models.CASCADE, limit_choices_to={'is_active': True},
                                     help_text="Select a component to link to this signature")
    signature_url = models.URLField(
        help_text="The digital signature / address of this object on the block chain. Please refer to the README on registering components on the block chain.")
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.component.master_component.name

    def __str__(self):
        return self.component.master_component.name


class AircraftAssembly(models.Model):
    """This object stores all the details of a assembly / manufacturing processes for a drone """
    
    STATUS_CHOICES = ((0, _('In Progress')), (1, _('Parts needed')),(2, _('Complete')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    model = models.ForeignKey(AircraftModel, on_delete=models.CASCADE, help_text="Assign a model to this aircraft")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1,
                                 help_text="Set the status of this drone assembly, only complete assemblies maybe added to the drone")

    components = models.ManyToManyField(AircraftComponent, related_name='aircraft_components',
                                        help_text="Set the components for this aircraft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return ' Model: ' +self.model.name + ' / Series: ' + self.model.series

    def __str__(self):
        return ' Model: ' +self.model.name + ' / Series: ' + self.model.series

class Aircraft(models.Model):
    STATUS_CHOICES = ((0, _('Inactive')), (1, _('Active')),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Associate a operator to this Aircraft")
    manufacturer = models.ForeignKey(Company, models.CASCADE,
                                     help_text="Associate a manufacturer in the database to this aircraft",limit_choices_to={'role':1})
    name = models.CharField(max_length=280, help_text="Set the internal name of the aircraft e.g. F1 #2")
    flight_controller_id = models.CharField(
        help_text="This is the Drone ID from the RFM, if there are spaces in the ID, remove them", max_length=140,
        validators=[validate_flight_controller_id])
    status = models.IntegerField(choices=STATUS_CHOICES, default=1,
                                 help_text="Set the status of this drone, if it is set as inactive, the GCS might fail and flight plans might not be able to load on the drone")

    final_assembly = models.OneToOneField(AircraftAssembly, on_delete=models.CASCADE, help_text="Assign a aircraft assembly to this aircraft, if you do not see a assembly, it means that you will need to create a new assembly first.", limit_choices_to={'status':2})
    photo = models.URLField(help_text="A URL of a photo of the drone",
                            default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class AircraftDetail(models.Model):
    ''' This model holds extended details of an aircraft '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    aircraft = models.OneToOneField(Aircraft, models.CASCADE, help_text="Choose the aircraft")

    is_registered = models.BooleanField(default=False,
                                        help_text="Set if the aircraft is registred with the Civil Aviation Authority")

    registration_mark = models.CharField(max_length=10, blank=True, null=True,
                                         help_text="Set the registration mark for this aircraft, if applicable")
    commission_date = models.DateTimeField(blank=True, null=True)
    digital_sky_uin_number = models.CharField(max_length=140,
                                              help_text="Get a UIN number for this aircraft using the Digital Sky Portal",
                                              blank=True, null=True)

    identification_photo = models.URLField(blank=True, null=True,
                                           help_text="A URL to a photo of the drone ID or other identifying image of the drone.")
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.aircraft.name + ' Extended Details'

    def __str__(self):
        return self.aircraft.name + ' Extended Details'
