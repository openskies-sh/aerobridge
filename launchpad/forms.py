from registry.models import AircraftMasterComponent, Person, Address, Operator, Aircraft, Manufacturer, Firmware, Contact, Pilot, Activity, Authorization, AircraftDetail, AircraftComponentSignature, AircraftComponent,AircraftModel

from gcs_operations.models import FlightOperation, FlightLog, FlightPlan, FlightPermission
from pki_framework.models import AerobridgeCredential
from django import forms

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import json
import geojson
import arrow
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import AccordionGroup
from crispy_bootstrap5.bootstrap5 import FloatingField, BS5Accordion


KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('OTHER')),)
TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('RFM KEY')),(4, _('OTHER')),)

# books/forms.py


class PersonCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("first_name"),
                        FloatingField("middle_name"),
                        FloatingField("last_name"),
                        FloatingField("email"),
                        FloatingField("phone_number"),
                        FloatingField("country"),
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("documents"),                        
                        FloatingField("date_of_birth")
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Person'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'people-list' %}" role="button">Cancel</a>""")
                    )
                )     

    class Meta:
        model = Person
        fields = '__all__'
        
class AddressCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("address_line_1"),
                        FloatingField("address_line_2"),
                        FloatingField("address_line_3"),
                        FloatingField("postcode"),                        
                        FloatingField("city"),
                        FloatingField("state"),
                        FloatingField("country"),
                        ),                                
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Address'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'addresses-list' %}" role="button">Cancel</a>""")
                    )
                )     

    class Meta:
        model = Address
        fields = '__all__'


class OperatorCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("company_name"),
                        FloatingField("website"),
                        FloatingField("email"),
                        FloatingField("phone_number"),
                        FloatingField("operator_type"),
                        FloatingField("address"),
                        ),
                    AccordionGroup("Optional Information",
                        "operational_authorizations",
                        "authorized_activities",
                        FloatingField("insurance_number"),
                        FloatingField("company_number"),
                        FloatingField("vat_number"),
                        FloatingField("country"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Operator'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'operators-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Operator
        exclude = ('expiration',)

class AircraftCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("manufacturer"),
                        FloatingField("category"),
                        FloatingField("flight_controller_id"),
                        FloatingField("status"),
                        FloatingField("photo"),
                        FloatingField("name")
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircrafts-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     
     

    class Meta:
        model = Aircraft
        fields = ('operator','manufacturer', 'name','flight_controller_id', 'category','status','photo',)

class AircraftDetailCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("aircraft"),
                        FloatingField("mass"),
                        FloatingField("sub_category"),
                        FloatingField("max_certified_takeoff_weight"),
                        FloatingField("max_height_attainable"),
                        FloatingField("is_registered"),
                        
                        ),
                    AccordionGroup("Optional Information",                        
                        FloatingField("commission_date"),
                        FloatingField("icao_aircraft_type_designator"),
                        FloatingField("registration_mark"),
                        FloatingField("digital_sky_uin_number"),
                        FloatingField("operating_frequency"),
                        FloatingField("manufactured_at"),
                        FloatingField("documents"),                        
                        FloatingField("type_certificate"),
                        FloatingField("identification_photo"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Details'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircrafts-list' %}" role="button">Cancel</a>""")
                    )
                )     
    
    class Meta:
        model = AircraftDetail
        fields = '__all__'

class AircraftComponentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("supplier_part_id"),
                        FloatingField("master_component"),
                        FloatingField("custody_status"),
                        FloatingField("custody_on"),
                        ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Component Details'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-components-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    class Meta:
        model = AircraftComponent
        fields = '__all__'

class AircraftMasterComponentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("family"),
                        FloatingField("drawing"),
                        ),
                  
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Master Component'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-master-components-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    class Meta:
        model = AircraftMasterComponent
        fields = '__all__'

class AircraftModelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("popular_name"),
                        FloatingField("master_components"),
                        FloatingField("max_endurance"),
                        FloatingField("max_range"),
                        FloatingField("max_speed"),
                        FloatingField("dimension_length"),
                        FloatingField("dimension_breadth"),
                        FloatingField("dimension_height"),
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("series"),            
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Model'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-models-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    class Meta:
        model = AircraftModel
        fields = '__all__'

class AircraftComponentSignatureCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("component"),
                        FloatingField("signature_url"),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Component Signature Details'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-components-signature-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     
        )

    class Meta:
        model = AircraftComponentSignature
        fields = '__all__'

class ManufacturerCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("full_name"),
                        FloatingField("common_name"),
                        FloatingField("address"),
                        FloatingField("acronym"),
                        FloatingField("role"),
                        FloatingField("country"),
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("digital_sky_id"),
                        FloatingField("documents"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Manufacturer'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'manufacturers-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Manufacturer
        fields =('full_name','common_name', 'address','acronym', 'role','acronym','role','country','digital_sky_id', 'documents')

class FirmwareCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("binary_file_url"),
                        FloatingField("public_key"),
                        FloatingField("version"),
                        FloatingField("manufacturer"),
                        FloatingField("friendly_name"),
                        "is_active",
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Firmware'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'firmwares-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
   
        

    class Meta:
        model = Firmware
        fields = '__all__'

class FlightPlanCreateForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        "geo_json",
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Flight Plan'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightplans-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )

    def clean_geo_json(self):
        gj = self.cleaned_data.get('geo_json', False)  
        
        try:
            parsed_geojson = geojson.loads(json.dumps(gj))
        except Exception as ve:      
            raise ValidationError(_("Not a valid GeoJSON, please enter a valid GeoJSON object %s "% ve))
        try:            
            assert parsed_geojson.is_valid
        except AssertionError as ae:             
            raise ValidationError(_("Not a valid GeoJSON, please enter a valid GeoJSON object %s" % ae))
        except AttributeError as atr_e:             
            raise ValidationError(_("Valid GeoJSON not provided"))
        else:
            return gj

        
    class Meta:
        model = FlightPlan
        exclude = ('is_editable','plan_file_json',)
        

class FlightPermissionCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FlightPermissionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operation"),
                        ),
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Permission'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightpermissions-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
    class Meta:
        model = FlightPermission
        fields = ('operation',)
    

class FlightLogCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (FlightLogCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['operation'].queryset = FlightOperation.objects.filter(is_editable=True)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operation"),
                        FloatingField("raw_log"),
                        ),
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Log'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightlogs-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
     
    class Meta:
        model = FlightLog
        fields = ('operation','raw_log',)
        

class FlightOperationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super (FlightOperationCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['flight_plan'].queryset = FlightPlan.objects.filter(is_editable=True)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("drone"),
                        FloatingField("flight_plan"),
                        FloatingField("purpose"),
                        FloatingField("operator"),
                        FloatingField("pilot"),
                        "start_datetime",
                        "end_datetime",
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("type_of_operation")                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Operation'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightoperations-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
     
    
    def clean(self):
        cleaned_data = super().clean()
        s_date = cleaned_data.get("start_datetime")
        e_date = cleaned_data.get("end_datetime")
        start_date = arrow.get(s_date)
        end_date = arrow.get(e_date)
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    class Meta:
        model = FlightOperation
        exclude = ('is_editable','created_at',)
        widgets = {            
            'start_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time', 'type':'datetime-local'}),
            'end_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time ', 'type':'datetime-local'}),
        }
        help_texts = {
            'flight_plan': 'If a flight log is signed and is associated with a plan, that plan will not show here',
        }

class ContactCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("person"),
                        FloatingField("address"),
                        FloatingField("role_type")
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Contact'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'contacts-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )

    
    class Meta:
        model = Contact
        fields = '__all__'


class PilotCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("person"),
                        FloatingField("photo"),
                        
                        ),
                        
                    AccordionGroup("Optional Information",
                        FloatingField("photo"),
                        FloatingField("identification_photo"),
                        FloatingField("tests"),
                        ),                                 
                    ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Pilot'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'pilots-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
    
    class Meta:
        model = Pilot
        fields = '__all__'

# class DigitalSkyLogCreateForm(forms.ModelForm):
#     class Meta:
#         model = DigitalSkyLog
#         fields = '__all__'

# class DigitalSkyTransactionCreateForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

class AuthorizationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("title"),
                        FloatingField("operation_max_height"),
                        FloatingField("operation_altitude_system"),
                        FloatingField("airspace_type"),
                        FloatingField("operation_area_type"),
                        FloatingField("risk_type"),
                        FloatingField("authorization_type"),
                        "permit_to_fly_above_crowd",
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Activity'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
    class Meta:
        model = Authorization
        # exclude = ('is_created',)
        fields = '__all__'
        
class ActivityCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        'activity_type'
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Activity'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Activity
        # exclude = ('is_created',)
        fields = '__all__'
        
class TokenCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("token_type"),
                        FloatingField("extension"),
                        FloatingField("association"),
                        "credential"
                    ),
                    AccordionGroup("Optional Information",
                        FloatingField("aircraft"),
                        FloatingField("manufacturer"),
                        FloatingField("operator"),
                        'is_active'
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Credentials'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'credentials-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    credential = forms.CharField(widget=forms.Textarea, help_text="Paste the credential as plain text here")
    class Meta:
        model = AerobridgeCredential
        # fields = '__all__'
        exclude = ('token',)
        
        
        
class CustomCloudFileCreateForm(forms.Form):
    
    UPLOAD_TYPE = (
        ('logs', 'Logs'),
        ('documents', 'Documents'),
        ('other', 'Other'),
    )
    file = forms.FileField()
    file_type = forms.CharField(max_length=140,widget=forms.Select(choices=UPLOAD_TYPE))
    name = forms.CharField()
        
class CutsomTokenCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    token_type = forms.IntegerField(widget=forms.Select(choices=TOKEN_TYPE),
    )
    association = forms.IntegerField(widget=forms.Select(choices=KEY_ENVIRONMENT),
    )
    token = forms.CharField(widget = forms.TextInput())