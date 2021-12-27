from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from . import countries 
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
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
    return datetime.combine( date.today() + relativedelta(months=+24), datetime.min.time()).replace(tzinfo=timezone.utc)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$', message="No special characters allowed in this field.")


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, help_text="The first name of the person added to the database")
    middle_name = models.CharField(max_length=30, null = True, blank = True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(help_text="Associate a email address with the person, this field is required")    
    phone_number = models.CharField(validators=[phone_regex], max_length=17, help_text="Associate a phone number with this person")
    identification_document = models.URLField(blank=True, null=True,validators=[validate_url,], default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf")
    social_security_number = models.CharField(max_length=25, blank=True, null=True, help_text="If social security / identification number is avaialble associate it with a person")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Assign a date of birth with this person")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.first_name +' ' + self.last_name

    def __str__(self):
        return self.first_name +' ' + self.last_name


class Address(models.Model):
    STATE_CHOICES = (("AN",_("Andaman and Nicobar Islands")),("AP",_("Andhra Pradesh")),("AR",_("Arunachal Pradesh")),("AS",_("Assam")),("BR",_("Bihar")),("CG",_("Chandigarh")),("CH",_("Chhattisgarh")),("DN",_("Dadra and Nagar Haveli")),("DD",_("Daman and Diu")),("DL",_("Delhi")),("GA",_("Goa")),("GJ",_("Gujarat")),("HR",_("Haryana")),("HP",_("Himachal Pradesh")),("JK",_("Jammu and Kashmir")),("JH",_("Jharkhand")),("KA",_("Karnataka")),("KL",_("Kerala")),("LA",_("Ladakh")),("LD",_("Lakshadweep")),("MP",_("Madhya Pradesh")),("MH",_("Maharashtra")),("MN",_("Manipur")),("ML",_("Meghalaya")),("MZ",_("Mizoram")),("NL",_("Nagaland")),("OR",_("Odisha")),("PY",_("Puducherry")),("PB",_("Punjab")),("RJ",_("Rajasthan")),("SK",_("Sikkim")),("TN",_("Tamil Nadu")),("TS",_("Telangana")),("TR",_("Tripura")),("UP",_("Uttar Pradesh")),("UK",_("Uttarakhand")),("WB",_("West Bengal")))
                     
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_1 = models.CharField(max_length=140)
    address_line_2 = models.CharField(max_length=140,blank=True, null=True)
    address_line_3 = models.CharField(max_length=140,blank=True, null=True)
    postcode = models.CharField(_("post code"), max_length=10)
    city = models.CharField(max_length=140, help_text="Set a city for this address")
    state = models.CharField(max_length=2, blank=True, null=True , choices=STATE_CHOICES, help_text="Pick a state, at the moment only Indian States are configured.")
    country = models.CharField(max_length = 2, choices=countries.COUNTRY_CHOICES_ISO3166, default = 'IN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.address_line_1 

    def __str__(self):
        return self.address_line_1 


# Create your models here.
class Activity(models.Model):
    ACTIVITYTYPE_CHOICES = ((0, _('NA')),(1, _('Open')),(2, _('Specific')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, help_text="Set a name for this activity")
    activity_type = models.IntegerField(choices=ACTIVITYTYPE_CHOICES, default = 0, help_text="Set the activity type and the airspace")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.name

    def __str__(self):
        return self.name

class Authorization(models.Model):
    AREATYPE_CHOICES = ((0, _('Unpopulated')),(1, _('Sparsely Populated')),(2, _('Densely Populated')),)
    RISKCLASS_CHOICES = ((0, _('NA')),(1, _('SAIL 1')),(2, _('SAIL 2')),(3, _('SAIL 3')),(4, _('SAIL 4')),(5, _('SAIL 5')),(6, _('SAIL 6')),)
    AUTHTYPE_CHOICES = ((0, _('NA')),(1, _('Light UAS Operator Certificate')),(2, _('Standard Scenario Authorization')),)
    AIRSPACE_CHOICES = ((0, _('NA')),(1, _('Green')),(2, _('Amber')),(3, _('Red')),)
    ALTITUDE_SYSTEM = ((0, _('wgs84')),(1, _('amsl')),(2, _('agl')),(3, _('sps')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=140)
    operation_max_height = models.IntegerField(default = 0, help_text="Set the maximum authorized height for this authorization")
    operation_altitude_system = models.IntegerField(default =0, choices = ALTITUDE_SYSTEM, help_text="Set the altitude system")
    airspace_type = models.IntegerField(choices = AIRSPACE_CHOICES, default =0, help_text="Set the airspace type, if available")
    permit_to_fly_above_crowd = models.BooleanField(default = 0, help_text="Select if the company is permitted to fly above crowd")
    operation_area_type = models.IntegerField(choices=AREATYPE_CHOICES, default = 0,  help_text="Can the operator fly over crowds? ")
    risk_type = models.IntegerField(choices= RISKCLASS_CHOICES, default =0, help_text="If available, set the airspace risk type")
    authorization_type = models.IntegerField(choices= AUTHTYPE_CHOICES, default =0, help_text="Set the type of the authorization")
    end_date = models.DateTimeField(default = two_year_expiration, help_text="By default every authorization exipres in two years, you can set a different end date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.title

    def __str__(self):
        return self.title

class Operator(models.Model):    
    OPTYPE_CHOICES = ((0, _('NA')),(1, _('LUC')),(2, _('Non-LUC')),(3, _('AUTH')),(4, _('DEC')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=28,help_text="Official Name of the company as in the Company Registration Office", validators = [no_special_characters_regex,])
    website = models.URLField(help_text="Put official URL of the company, if none is available then a manufacturers public facing URL is necessary")
    email = models.EmailField(help_text="Contact email for support and other queries")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) #        
    expiration = models.DateTimeField(default = two_year_expiration)
    operator_type = models.IntegerField(choices=OPTYPE_CHOICES, default = 0, help_text="Choose what kind of operator this is, classify the operator based on capabilites, use the adminsitration panel to add additional operator categories")
    address = models.ForeignKey(Address, models.CASCADE,help_text="Select the official address for the company")
    operational_authorizations = models.ManyToManyField(Authorization, related_name = 'operational_authorizations',help_text="Choose what kind of authorization this operator posseses, to add additional authorizations, use the administration panel")
    authorized_activities = models.ManyToManyField(Activity, related_name = 'authorized_activities',help_text="Related to Authorization, select the kind of activities that this operator is allowed to conduct, you can add additional activities using the administration panel" )
    vat_number = models.CharField(max_length=25,default="VAT-TMP",validators = [no_special_characters_regex,], blank = True, null=True, help_text="VAT / Tax number if available")
    insurance_number = models.CharField(max_length=25,default = "INS-TMP",validators = [no_special_characters_regex,], blank = True, null=True, help_text="Insurance number if avaialble")
    company_number = models.CharField(max_length=25, default='CO-TMP',validators = [no_special_characters_regex,], blank = True, null=True, help_text="Company number if available ")
    country = models.CharField(max_length = 2, choices=countries.COUNTRY_CHOICES_ISO3166, default = 'IN', help_text="At the moment only India is configured, you can setup your own country")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_address(self):
        full_address = '%s, %s, %s, %s %s, %s' % (self.address.address_line_1, self.address.address_line_2,self.address.address_line_3,self.address.city, self.address.state, self.address.country)
        return full_address
       
    def __unicode__(self):
       return self.company_name

    def __str__(self):
        return self.company_name

class Contact(models.Model):
    ROLE_CHOICES = ((0, _('Other')),(1, _('Responsible')))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, related_name='person_contact', help_text="Set a operator for this contact")    
    person = models.ForeignKey(Person, models.CASCADE, help_text="Associate a person for this contact")    
    address = models.ForeignKey(Address, models.CASCADE, help_text="Add a address for this contact")
    role_type = models.IntegerField(choices=ROLE_CHOICES, default = 0, help_text="A contact may or may not be legally responsible officer within a company, specify if the contact is responsisble (legally) for operations in the company")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name

    def __str__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name


class Test(models.Model):
    TESTTYPE_CHOICES = ((0, _('Remote pilot online theoretical competency')),(1, _('Certificate of remote pilot competency')),(2, _('Other')),)
    TAKEN_AT_CHOICES = ((0, _('Online Test')),(1, _('In Authorized Test Center')),(2, _('Other')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_type = models.IntegerField(choices = TESTTYPE_CHOICES, default =0, help_text="Specify the type of test")
    taken_at = models.IntegerField(choices = TAKEN_AT_CHOICES, default =0, help_text="Specify where this test was taken")
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
    person = models.OneToOneField(Person, models.CASCADE, help_text="Assign this pilot to a person object in the database")
    photo = models.URLField(blank=True, null=True,validators=[validate_url,], help_text="A URL to link to a photo of the pilot")
    
    address = models.ForeignKey(Address, models.CASCADE, help_text="Assign a address to this Pilot")
    identification_photo = models.URLField(default='https://github.com/openskies-sh/aerobridge/blob/master/sample-data/id-card-sample.jpeg',validators=[validate_url,], help_text = "A URL to link to a photo of and ID document of the pilot")
        
    tests = models.ManyToManyField(Test, through ='TestValidity', help_text="Specify the tests if any the pilot has taken")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =0, help_text="Is this pilot active? If he is not working for the company or has moved on, set it as inactive")

    def __unicode__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name

    def __str__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name


class TestValidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, models.CASCADE)
    pilot = models.ForeignKey(Pilot, models.CASCADE)
    taken_at = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)

class TypeCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_certificate_id = models.CharField(max_length = 280)
    type_certificate_issuing_country = models.CharField(max_length = 280)
    type_certificate_holder = models.CharField(max_length = 140)
    type_certificate_holder_country = models.CharField(max_length = 140)
    
    def __unicode__(self):
       return self.type_certificate_holder

    def __str__(self):
       return self.type_certificate_holder


class Manufacturer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length = 140,help_text="Full legal name of the manufacturing entity")
    common_name = models.CharField(max_length = 140, help_text="Common name for the manufacturer e.g. Skydio")
    address = models.ForeignKey(Address, models.CASCADE, blank= True, null=True, help_text="Assign a address to this manufacturers")
    acronym = models.CharField(max_length =10,help_text="If you use a acronym for this manufacturer, you can assign it here")
    role = models.CharField(max_length = 140, help_text="e.g. Reseller, distributor, OEM etc.")
    country = models.CharField(max_length =3, help_text="The three-letter ISO 3166-1 country code where the manufacturer is located")
    digital_sky_id = models.CharField(max_length=140, default="NA", help_text="Use the Digital Sky portal to create a Manufacturer profile and get an ID, paste it here")

    cin_document = models.URLField(help_text ='Link to certificate of Incorporation issued by ROC, MCA', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf')
    gst_document = models.URLField(help_text='Link to GST certification document', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    pan_card_document = models.URLField(help_text='URL of Manufacturers PAN Card scan', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    security_clearance_document = models.URLField(help_text='Link to Security Clearance from Ministry of Home Affairs', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    eta_document = models.URLField(help_text='Link to Equipment Type Approval (ETA) from WPC Wing', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
       return self.common_name

    def __str__(self):
       return self.common_name

  
class Firmware(models.Model):
    ''' A model for custom firmware '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    binary_file_url= models.URLField(help_text="Enter a url from where the firmware can be downloaded")
    public_key = models.TextField(help_text="Enter a SHA / Digest or public key to test used to secure the firmware")
    version = models.CharField(max_length=25, help_text="Set a semantic version for the firmware version")  
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE, help_text = "Associate a manufacturer to the firmware")
    friendly_name = models.CharField(max_length=140, help_text="Give it a friendly name e.g. May-2021 1.2 release")
    is_active = models.BooleanField(default=False, help_text="Set if the firmware is active, don't forget to mark old firmware as inactive")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
       return self.version

    def __str__(self):
        return self.version 
    
  
class Aircraft(models.Model):
    AIRCRAFT_CATEGORY = ((0, _('Other')),(1, _('FIXED WING')),(2, _('ROTORCRAFT')),(3, _('LIGHTER-THAN-AIR')),(4, _('HYBRID LIFT')),(5, _('MICRO')),(6, _('SMALL')),(7, _('MEIDUM')),(8, _('Large')),)
    STATUS_CHOICES = ((0, _('Inactive')),(1, _('Active')),)  
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Associate a operator to this Aircraft")
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE, help_text= "Associate a manufacturer in the database to this aircraft")
    model = models.CharField(max_length = 280, help_text="Set the model of the aircraft")
    flight_controller_id = models.CharField(help_text= "This is the Drone ID from the RFM, if there are spaces in the ID, remove them",max_length=140, validators=[validate_flight_controller_id])    
    category = models.IntegerField(choices=AIRCRAFT_CATEGORY, default = 0, help_text="Set the category for this aircraft, use the closest aircraft type")
    status = models.IntegerField(choices=STATUS_CHOICES, default = 1, help_text="Set the status of this drone, if it is set as inactive, the GCS might fail and flight plans might not be able to load on the drone")

    photo = models.URLField(help_text="A URL of a photo of the drone", default="https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords()

    def __unicode__(self):
        return self.operator.company_name +' ' + self.model

    def __str__(self):
        return self.operator.company_name +' ' + self.model

# class AircraftComponent(models.Model):
# ''' This class stores details of componentes of a aircraft ''' 
#     COMPONENT_TYPE = ((0, _('Frame')),(1, _('Motors')),(2, _('Electronic Speed Controller')),(3, _('Flight Controller')),(4, _('Power Distribution Board')),(5, _('Battery')),(6, _('Propellors')),(7, _('Camera')),(8, _('GPS')),)

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=140, null=True, blank=True)
#     photo = models.URLField(blank=True, null=True, help_text="A URL to a photo of the component.")   
#     purchased_on =  models.DateTimeField(blank= True, null= True, help_text="Enter a date when this component was purchased")

#     history = HistoricalRecords()

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)        


class AircraftDetail(models.Model): 
    ''' This model holds extended details of an aircraft '''
    AIRCRAFT_SUB_CATEGORY = ((0, _('Other')),(1, _('AIRPLANE')),(2, _('NONPOWERED GLIDER')),(3, _('POWERED GLIDER')),(4, _('HELICOPTER')),(5, _('GYROPLANE')),(6, _('BALLOON')),(7, _('AIRSHIP')),(8, _('UAV')),(9, _('Multirotor')),(10, _('Hybrid')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    aircraft = models.OneToOneField(Aircraft, models.CASCADE, help_text="Choose the aircraft")
    mass = models.IntegerField(default= 300, help_text="Set the vehicle's mass in gms.")
    sub_category = models.IntegerField(choices=AIRCRAFT_SUB_CATEGORY, default = 7, help_text='')
    max_certified_takeoff_weight = models.DecimalField(decimal_places = 3, max_digits=10, default = 0.00, help_text="Set the takeoff weight for the aircraft in gms.")
    max_height_attainable =  models.DecimalField(decimal_places = 3, max_digits=10, default = 0.00,  help_text="Set the max attainable height in meters")    
    is_registered = models.BooleanField(default=False, help_text="Set if the aircraft is registred with the Civil Aviation Authority")
    max_endurance = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the endurance in minutes")
    max_range = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the range in kms for the drone")
    max_speed = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the maximum speed in km/hr.")
    dimension_length = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the length of the drone in cms") 
    dimension_breadth = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the breadth of the drone in cms")
    dimension_height = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00, help_text="Set the height of the drone in cms")


    popular_name = models.CharField(max_length = 280, blank= True, null=True, help_text="Enter popular name for this aircraft")    
    make = models.CharField(max_length = 280, blank= True, null=True, help_text="Enter aircraft make ")    
    master_series = models.CharField(max_length = 280, blank= True, null=True, help_text="Specify the master series, if available")    
    series = models.CharField(max_length = 280, blank= True, null=True, help_text="Enter aircraft production series, if available")    
    icao_aircraft_type_designator = models.CharField( blank= True, null=True,max_length =4, default = '0000', help_text="If available you can specify the type designator, see https://www.icao.int/publications/doc8643/pages/search.aspx")
    registration_mark = models.CharField(max_length= 10, blank= True, null=True, help_text="Set the registration mark for this aircraft, if applicable")
    commission_date = models.DateTimeField(blank= True, null= True)
    digital_sky_uin_number = models.CharField(max_length=140, help_text="Get a UIN number for this aircraft using the Digital Sky Portal",blank= True, null= True)    
    operating_frequency = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00,blank= True, null= True)    
    manufactured_at = models.DateTimeField(help_text="Set the date when the drone was manufactured",blank= True, null= True)    
    dot_permission_document = models.URLField(blank=True, null=True, help_text="Link to Purchased RPA has ETA from WPC Wing, DoT for operating in the de-licensed frequency band(s). Such approval shall be valid for a particular make and model", default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    operations_manual_document = models.URLField(blank=True, null=True, help_text="Link to Operation Manual Document", default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    type_certificate = models.ForeignKey(TypeCertificate, models.CASCADE, blank= True, null= True, help_text="Set the type certificate if available for the drone")
    
    identification_photo = models.URLField(blank=True, null=True, help_text="A URL to a photo of the drone ID or other identifying image of the drone.")
    history = HistoricalRecords()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.aircraft.model + ' Extended Details'
    def __str__(self):
        return self.aircraft.model + ' Extended Details'