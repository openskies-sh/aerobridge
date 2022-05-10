from decimal import Decimal
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
from common.settings import currency_code_default as cc_default
from common.validators import validate_currency_code, validate_url, validate_flight_controller_id
from common.status_codes import BuildStatus, StatusCode, StockStatus
from django.db.models import Sum, Q
from moneyed import CURRENCIES
from django.core.validators import MinValueValidator
from common.helpers import normalize
from django.db.models.functions import Coalesce
# Source https://stackoverflow.com/questions/63830942/how-do-i-validate-if-a-django-urlfield-is-from-a-specific-domain-or-hostname

def two_year_expiration():
    return datetime.combine(date.today() + relativedelta(months=+24), datetime.min.time()).replace(tzinfo=timezone.utc)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$',
                                             message="No special characters allowed in this field.")

class AerobridgeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(help_text="Give a name for this document")
    url = models.URLField(blank=True, null=True, validators=[validate_url],
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
    (0, _('Supplier')), (1, _('Manufacturer')), (2, _('Operator')), (3, _('Customer')),(4, _('Assembler')), )

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=140, help_text="Full legal name of the manufacturing entity")
    common_name = models.CharField(max_length=140, help_text="Common name for the manufacturer e.g. Skydio")
    address = models.ForeignKey(Address, models.CASCADE, blank=True, null=True,
                                help_text="Assign a address to this manufacturers")
                                    
    country = models.CharField(max_length=3,
                               help_text="The three-letter ISO 3166-1 country code where the manufacturer is located")
    website = models.URLField(
        help_text="Put official URL of the company, if none is available then a manufacturers public facing URL is necessary", validators=[validate_url])
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
        # 
        return SupplierPart.objects.filter(Q(supplier=self.id) | Q(manufacturer_part__manufacturer=self.id))

    @property
    def manufactured_parts(self):
        """ Return SupplierPart objects which are supplied or manufactured by this company """
        return ManufacturerPart.objects.filter(Q(manufacturer=self.id))

    @property
    def supplied_parts(self):
        """ Return SupplierPart objects which are supplied or manufactured by this company """
        return SupplierPart.objects.filter(Q(supplier=self.id))
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
        
        return AircraftComponent.objects.filter(Q(supplier_part__supplier=self.id) | Q(supplier_part__manufacturer_part__manufacturer=self.id)).all()

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
    binary_file_url = models.URLField(help_text="Enter a url from where the firmware can be downloaded",validators=[validate_url])
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text= "Specify the company associated with this operator")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_address(self):
        full_address = '%s, %s, %s, %s %s, %s' % (
        self.address.address_line_1, self.address.address_line_2, self.address.address_line_3, self.address.city,
        self.address.state, self.address.country)
        return full_address

    def __unicode__(self):
        return self.company.full_name

    def __str__(self):
        return self.company.full_name

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


class Pilot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Assign this pilot to a operator")
    person = models.OneToOneField(Person, models.CASCADE,
                                  help_text="Assign this pilot to a person object in the database")
    photo = models.URLField(blank=True, null=True, validators=[validate_url],
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
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company.common_name

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' : ' + self.operator.company.common_name

class TestValidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, models.CASCADE)
    pilot = models.ForeignKey(Pilot, models.CASCADE)
    taken_at = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)

class SupplierPartManager(models.Manager):
    """ Define custom SupplierPart objects manager
        The main purpose of this manager is to improve database hit as the
        SupplierPart model involves A LOT of foreign keys lookups
    """

    def get_queryset(self):
        # Always prefetch related models
        return super().get_queryset().prefetch_related(
            
            'supplier',
            'manufacturer_part__manufacturer',
        )



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
    drawing = models.URLField(blank=True, null=True, help_text="A URL to a photo of the component drawing.",validators =[validate_url])

    manufacturer = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name='master_component_manufacturer',
        limit_choices_to={
            'role': 1
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


    minimum_stock = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0)],
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
        default=False,
        verbose_name=_('Assembly'),
        help_text=_('Can this part be built from other parts?')
    )

    trackable = models.BooleanField(
        default=True, 
        verbose_name=_('Trackable'),
        help_text=_('Does this part have tracking for unique items?'))

    purchaseable = models.BooleanField(
        default=True,
        verbose_name=_('Purchaseable'),
        help_text=_('Can this part be purchased from external suppliers?'))

    salable = models.BooleanField(
        default=False,
        verbose_name=_('Salable'),
        help_text=_("Can this part be sold to customers?"))

    active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Is this part active?'))
    quantity_required_for_build = models.IntegerField(default = 1, help_text="Set the quantity reqired ")
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

    @property
    def total_stock(self):
        """
        Return the total available stock.
        - This subtracts stock which is already allocated to builds
        """

        total = self.total_stock
        total -= self.allocation_count()

        return max(total, 0)

    @property
    def slugify_family(self):        
        return self.family

    @property
    def default_supplier(self):
        """ Get the default supplier part for this part (may be None).
        - If the part specifies a default_supplier, return that
        - If there is only one supplier part available, return that
        - Else, return None
        """
        
        manufacturer_part = ManufacturerPart.objects.get(master_component = self.id)
        default_supplier = SupplierPart.objects.get(manufacturer_part = manufacturer_part)
        # Default to None if there are multiple suppliers to choose from
        return default_supplier



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

    def build_order_allocations(self, **kwargs):
        """
        Return all 'BuildItem' objects which allocate this part to Build objects
        """

        

        queryset = AircraftAssembly.objects.all()

        queryset = queryset.filter(components__supplier_part__manufacturer_part__master_component=self)

        return queryset

    def build_order_allocation_count(self, **kwargs):
        """
        Return the total amount of this part allocated to build orders
        """

        query = self.build_order_allocations(**kwargs).aggregate(
            total=Coalesce(
                Sum(
                    'quantity',
                    output_field=models.DecimalField()
                ),
                0,
                output_field=models.DecimalField(),
            )
        )

        return query['total']

    def allocation_count(self, **kwargs):
        """
        Return the total quantity of stock allocated for this part,
        against both build orders and sales orders.
        """

        return sum(
            [
                self.build_order_allocation_count(**kwargs),                
            ],
        )

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

    def total_stock(self):
        """ Return all stock entries for this Part.

        - If this is a template part, include variants underneath this.

        Note: To return all stock-entries for all part variants under this one,
        we need to be creative with the filtering.
        """

        query = self.stock_items
        query = query.filter(AircraftComponent.IN_STOCK_FILTER)
        return query

    @property
    def total_stock(self):
        """ Return the total stock quantity for this part.
        - Part may be stored in multiple locations
        - If this part is a "template" (variants exist) then these are counted too
        """

        return self.total_stock.count()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_bom_items(self):
        """
        Return a queryset containing all BOM items for this part

        By default, will include inherited BOM items
        """

        queryset = AircraftAssembly.objects.filter(self.get_bom_item_filter())

        return queryset

    def get_bom_item_filter(self):
        """
        Returns a query filter for all BOM items associated with this Part.

        There are some considerations:

        a) BOM items can be defined against *this* part
        b) BOM items can be inherited from a *parent* part

        We will construct a filter to grab *all* the BOM items!

        Note: This does *not* return a queryset, it returns a Q object,
              which can be used by some other query operation!
              Because we want to keep our code DRY!

        """

        bom_filter = Q(master_component=self)

        return bom_filter


    def get_used_in_filter(self):
        """
        Return a query filter for all parts that this part is used in.

        There are some considerations:

        a) This part may be directly specified against a BOM for a part
        b) This part may be specifed in a BOM which is then inherited by another part

        Note: This function returns a Q object, not an actual queryset.
              The Q object is used to filter against a list of Part objects
        """

        # This is pretty expensive - we need to traverse multiple variant lists!
        # TODO - In the future, could this be improved somehow?

        # Keep a set of Part ID values
        model_set = set()

        # First, grab a list of all BomItem objects which "require" this part
        models = AircraftModel.objects.filter(master_components__in=self)

        for model in models:
            # Add the directly referenced part
            model_set.add(model)

        # Turn into a list of valid IDs (for matching against a Part query)
        model_ids = [part.pk for part in model_set]

        return Q(id__in=model_ids)

    def get_used_in(self, include_inherited=True):
        """
        Return a queryset containing all models this master component is used in.

        Includes consideration of inherited BOMs
        """
        return AircraftModel.objects.filter(self.get_used_in_filter())

    @property
    def has_bom(self):
        return self.get_bom_items().count() > 0

    def get_trackable_parts(self):
        """
        Return a queryset of all trackable parts in the BOM for this part
        """

        queryset = self.get_bom_items()
        queryset = queryset.filter(master_component__trackable=True)

        return queryset

    @property
    def has_trackable_parts(self):
        """
        Return True if any parts linked in the Bill of Materials are trackable.
        This is important when building the part.
        """

        return self.get_trackable_parts().count() > 0

    @property
    def bom_count(self):
        """ Return the number of items contained in the BOM for this part """
        return self.get_bom_items().count()

    @property
    def used_in_count(self):
        """ Return the number of part BOMs that this part appears in """
        return self.get_used_in().count()

    @property
    def supplier_count(self):
        """ Return the number of supplier parts available for this part """
        
        return self.suppliers.all().count()
    @property
    def has_suppliers(self):
        """ Return the number of supplier parts available for this part """
        return self.supplier_count > 0

    @property
    def suppliers(self):
        """ Return the number of supplier parts available for this part """
        return SupplierPart.objects.filter(Q(manufacturer_part__master_component=self.id))

    @property
    def manufacturer_count(self):
        """ Return the number of supplier parts available for this part """
        return self.manufacturer_parts.count()

    @property
    def manufacturers(self):
        """ Return the number of supplier parts available for this part """
        return ManufacturerPart.objects.filter(Q(master_component=self.id))

    @property
    def has_manufacturers(self):
        """ Return the number of supplier parts available for this part """
        return self.manufacturer_parts.all().count() > 0

    @property
    def has_pricing_info(self, internal=False):
        """ Return true if there is pricing information for this part """
        return self.get_price_range(internal=internal) is not None
    
    @property
    def get_price_info(self, quantity=1, buy=True, bom=True, internal=False):
        """ Return a simplified pricing string for this part

        Args:
            quantity: Number of units to calculate price for
            buy: Include supplier pricing (default = True)
            bom: Include BOM pricing (default = True)
            internal: Include internal pricing (default = False)
        """
        

        price_range = self.get_price_range(quantity, buy, bom, internal)

        if price_range is None:
            return None

        min_price, max_price = price_range

        if min_price == max_price:
            return min_price

        min_price = normalize(min_price)
        max_price = normalize(max_price)

        return "{a} - {b}".format(a=min_price, b=max_price)

    @property
    def total_stock(self):
        """ Return the total stock quantity for this part.

        - Part may be stored in multiple locations
        - If this part is a "template" (variants exist) then these are counted too
        """
        total_stock = AircraftComponent.objects.filter(supplier_part__manufacturer_part__master_component = self).count()
        
        return total_stock

# from https://github.com/inventree/InvenTree/blob/91cd76b55f2a8f6b34c56080442c0f7a09387c31/InvenTree/company/models.py 
class ManufacturerPart(models.Model):
    """ Represents a unique part as provided by a Manufacturer
    Each ManufacturerPart is identified by a MPN (Manufacturer Part Number)
    Each ManufacturerPart is also linked to a Part object.
    A Part may be available from multiple manufacturers
    Attributes:
        part: Link to the master Part
        manufacturer: Company that manufactures the ManufacturerPart
        MPN: Manufacture part number
        link: Link to external website for this manufacturer part
        description: Descriptive notes field
    """

    class Meta:
        unique_together = ('master_component', 'manufacturer', 'MPN')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master_component = models.ForeignKey(AircraftMasterComponent, on_delete=models.CASCADE,
                             related_name='manufacturer_parts',
                             verbose_name=_('Base Part'),
                             limit_choices_to={
                                 'purchaseable': True,
                             },
                             help_text=_('Select part'),
                             )

    manufacturer = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name='manufactured_parts',
        limit_choices_to={
            'role': 1
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
    @classmethod
    def create(cls, part, manufacturer, mpn, description, link=None):
        """ Check if ManufacturerPart instance does not already exist
            then create it
        """

        manufacturer_part = None

        try:
            manufacturer_part = ManufacturerPart.objects.get(part=part, manufacturer=manufacturer, MPN=mpn)
        except ManufacturerPart.DoesNotExist:
            pass

        if not manufacturer_part:
            manufacturer_part = ManufacturerPart(part=part, manufacturer=manufacturer, MPN=mpn, description=description, link=link)
            manufacturer_part.save()

        return manufacturer_part

    @property
    def pretty_name(self):
        s = ''
        s += self.master_component.name + ' | '

        if self.manufacturer:
            s += f'{self.manufacturer.full_name}'
            s += ' | '

        s += f'{self.MPN}'

        return s

    def __str__(self):
        return self.pretty_name

    def __unicode__(self):
        return self.pretty_name

class SupplierPart(models.Model):
    """ Represents a unique part as provided by a Supplier
    Each SupplierPart is identified by a SKU (Supplier Part Number)
    Each SupplierPart is also linked to a Part or ManufacturerPart object.
    A Part may be available from multiple suppliers
    Attributes:
        part: Link to the master Part (Obsolete)
        source_item: The sourcing item linked to this SupplierPart instance
        supplier: Company that supplies this SupplierPart object
        SKU: Stock keeping unit (supplier part number)
        link: Link to external website for this supplier part
        description: Descriptive notes field
        note: Longer form note field
        base_cost: Base charge added to order independent of quantity e.g. "Reeling Fee"
        multiple: Multiple that the part is provided in
        lead_time: Supplier lead time
        packaging: packaging that the part is supplied in, e.g. "Reel"
    """

    objects = SupplierPartManager()


    class Meta:
        unique_together = ('manufacturer_part', 'supplier', )


    def save(self, *args, **kwargs):
        """ Overriding save method to connect an existing ManufacturerPart """

        manufacturer_part = None

        if all(key in kwargs for key in ('manufacturer', 'MPN')):
            manufacturer_name = kwargs.pop('manufacturer')
            MPN = kwargs.pop('MPN')

            # Retrieve manufacturer part
            try:
                manufacturer_part = ManufacturerPart.objects.get(manufacturer__name=manufacturer_name, MPN=MPN)
            except (ValueError, Company.DoesNotExist):
                # ManufacturerPart does not exist
                pass

        if manufacturer_part:
            if not self.manufacturer_part:
                # Connect ManufacturerPart to SupplierPart
                self.manufacturer_part = manufacturer_part
            else:
                raise ValidationError(f'SupplierPart {self.__str__} is already linked to {self.manufacturer_part}')

        self.clean()
        self.validate_unique()

        super().save(*args, **kwargs)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE,
                                 related_name='supplied_parts',
                                 limit_choices_to={'role': 0},
                                 verbose_name=_('Supplier'),
                                 help_text=_('Select supplier'),
                                 )
    info_buy_url = models.URLField(default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf",validators=[validate_url],help_text="Specify a URL where this part can be bought")
    manufacturer_part = models.ForeignKey(ManufacturerPart, on_delete=models.CASCADE,
                                          blank=True, null=True,
                                          related_name='supplier_parts',
                                          verbose_name=_('Manufacturer Part'),
                                          help_text=_('Select manufacturer part'),
                                          )

    is_default = models.BooleanField(default=False, help_text="Set whether this is the default supplier / store for this master component")

    # TODO - Reimplement lead-time as a charfield with special validation (pattern matching).
    # lead_time = models.DurationField(blank=True, null=True)


    def get_price_range(self, quantity=1, buy=True, bom=True, internal=False, purchase=False):

        """ Return the price range for this part. This price can be either:

        - Supplier price (if purchased from suppliers)
        - BOM price (if built from other parts)
        - Internal price (if set for the part)
        - Purchase price (if set for the part)

        Returns:
            Minimum of the supplier, BOM, internal or purchase price. If no pricing available, returns None
        """

        # only get internal price if set and should be used
        if internal and self.has_internal_price_breaks:
            internal_price = self.get_internal_price(quantity)
            return internal_price, internal_price

        # only get purchase price if set and should be used
        if purchase:
            purchase_price = self.get_purchase_price(quantity)
            if purchase_price:
                return purchase_price

        buy_price_range = self.get_supplier_price_range(quantity) if buy else None
        bom_price_range = self.get_bom_price_range(quantity, internal=internal) if bom else None

        if buy_price_range is None:
            return bom_price_range

        elif bom_price_range is None:
            return buy_price_range

        else:
            return (
                min(buy_price_range[0], bom_price_range[0]),
                max(buy_price_range[1], bom_price_range[1])
            )

    purchase_price = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name=_('Purchase Price'),
        help_text=_('Single unit purchase price at time of purchase'),
    )

    @property
    def order_price(self, quantity= 1):
        print('here')
        if not quantity:
            quantity = self.manufacturer_part.master_component.quantity_required_for_build
        cost = self.purchase_price * quantity
        return cost

    def on_order(self):
        """ Return the total quantity of items currently on order.
        Subtract partially received stock as appropriate
        """

        totals = self.open_orders().aggregate(Sum('quantity'), Sum('received'))

        # Quantity on order
        q = totals.get('quantity__sum', 0)

        # Quantity received
        r = totals.get('received__sum', 0)

        if q is None or r is None:
            return 0
        else:
            return max(q - r, 0)

    @property
    def pretty_name(self):
        s = ''

        if self.manufacturer_part.master_component.name:
            s += f'{self.manufacturer_part.master_component.name}'
            s += ' from '

        s += f'{self.supplier.common_name} '

        return s

    def __str__(self):
        return self.pretty_name

    def __unicode__(self):
        return self.pretty_name

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
    documents = models.ManyToManyField(AerobridgeDocument, blank=True, help_text="Associate any existing documents to this series / model")                                                                   
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
    
    """
    A AircraftComponent object represents a quantity of physical instances of a part.

    """
    IN_STOCK_FILTER = Q(
        quantity__gt=0,        
        status__in=StockStatus.AVAILABLE_CODES
    )    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    custody_on = models.DateTimeField(blank=True, null=True,
                                      help_text="Enter a date when this component was in custody of the manufacturer")
    is_active = models.BooleanField(default=True)


    history = HistoricalRecords()

    supplier_part = models.ForeignKey(
        SupplierPart, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Supplier Part'),
        help_text=_('Select a matching supplier part for this stock item')        
    )

    description = models.CharField(
        max_length=140, blank=True, null=True,
        verbose_name=_('Description'),
        help_text=_('Internal part description')
    )

    updated = models.DateField(auto_now=True, null=True)

    stocktake_date = models.DateField(blank=True, null=True)

    review_needed = models.BooleanField(default=False)

    status = models.PositiveIntegerField(
        default=StockStatus.OK,
        choices=StockStatus.items(),
        validators=[MinValueValidator(0)])

    purchase_price = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name=_('Purchase Price'),
        help_text=_('Single unit purchase price at time of purchase'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def component_common_name(self):
        items = []
        items.append(self.description)
        if self.supplier_part:
            if self.supplier_part.manufacturer_part:
                items.append(self.supplier_part.manufacturer_part.master_component.name)
        # print(items)
        return ' | '.join(items)

    @property
    def component_category(self):
        items = []
        
        if self.supplier_part:
            if self.supplier_part.manufacturer_part:
                items.append(self.supplier_part.manufacturer_part.master_component.get_family_display())
        # print(items)
        return '  '.join(items)


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


    def __unicode__(self):
        return self.component_common_name
        
    def __str__(self): 
        return self.component_common_name


class AircraftComponentSignature(models.Model):
    ''' This model saves information about the component signature on a the block chain '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.OneToOneField(AircraftComponent, on_delete=models.CASCADE, limit_choices_to={'is_active': True},
                                     help_text="Select a component to link to this signature")
    signature_url = models.URLField(
        help_text="The digital signature / address of this object on the block chain. Please refer to the README on registering components on the block chain.",validators= [validate_url])
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
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Associate a operator company with this Aircraft")
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
                            default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf",validators=[validate_url])
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
                                           help_text="A URL to a photo of the drone ID or other identifying image of the drone.", validators = [validate_url])
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.aircraft.name + ' Extended Details'

    def __str__(self):
        return self.aircraft.name + ' Extended Details'
