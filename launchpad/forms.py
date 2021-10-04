from registry.models import Person, Address, Operator, Aircraft, Manufacturer, Firmware, Contact, Pilot, Engine, Activity, Authorization
from digitalsky_provider.models import DigitalSkyLog
from gcs_operations.models import FlightOperation, FlightLog, FlightPlan, FlightPermission, Transaction, CloudFile
from pki_framework.models import AerobridgeCredential
from django import forms
from django.forms import widgets, Textarea
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import geojson
import arrow

KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('OTHER')),)
TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('RFM KEY')),(4, _('OTHER')),)

# books/forms.py


class PersonCreateForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = '__all__'
        
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class OperatorCreateForm(forms.ModelForm):

    class Meta:
        model = Operator
        exclude = ('expiration',)

class AircraftCreateForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        exclude = ('is_registered','type_certificate','make','model', 'series', 'master_series', 'registration_mark', 'icao_aircraft_type_designator', 'commission_date','operating_frequency','engine','manufactured_at','photo', 'photo_small', 'digital_sky_uin_number','identification_photo', 'identification_photo_small','popular_name',)

class ManufacturerCreateForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FirmwareCreateForm(forms.ModelForm):
    class Meta:
        model = Firmware
        fields = '__all__'

class FlightPlanCreateForm(forms.ModelForm):    
    
    def clean(self):
        cleaned_data = super().clean()
        s_date = cleaned_data.get("start_datetime")
        e_date = cleaned_data.get("end_datetime")
        start_date = arrow.get(s_date)
        end_date = arrow.get(e_date)
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    def clean_geo_json(self):
        gj = self.cleaned_data.get('geo_json', False)        
        try:
            validated_gj = geojson.loads(gj)
        except Exception as ve:                        
            raise ValidationError(_("Not a valid GeoJSON, please enter a valid GeoJSON object"))
        else:
            return gj

    class Meta:
        model = FlightPlan
        exclude = ('is_editable',)
        widgets = {            
            'start_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time', 'type':'datetime-local'}),
            'end_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time ', 'type':'datetime-local'}),
        }

class FlightPermissionCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    super(FlightPermissionCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['is_successful'].widget.attrs['disabled'] = True
    #    self.fields['artefact'].widget.attrs['disabled'] = True

    class Meta:
        model = FlightPermission
        fields = ('operation',)
        

class FlightLogCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (FlightLogCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['operation'].queryset = FlightOperation.objects.filter(is_editable=True)

    class Meta:
        model = FlightLog
        fields = ('operation','raw_log',)
        

class FlightOperationCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (FlightOperationCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['flight_plan'].queryset = FlightPlan.objects.filter(is_editable=True)

    class Meta:
        model = FlightOperation
        exclude = ('is_editable',)
        help_texts = {
            'flight_plan': 'If a flight log is signed and is associated with a plan, that plan will not show here',
        }

class ContactCreateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class PilotCreateForm(forms.ModelForm):
    class Meta:
        model = Pilot
        fields = '__all__'

class DigitalSkyLogCreateForm(forms.ModelForm):
    class Meta:
        model = DigitalSkyLog
        fields = '__all__'

class DigitalSkyTransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class EngineCreateForm(forms.ModelForm):
    class Meta:
        model = Engine
        fields = '__all__'
        

class AuthorizationCreateForm(forms.ModelForm):
    class Meta:
        model = Authorization
        # exclude = ('is_created',)
        fields = '__all__'
        
class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        # exclude = ('is_created',)
        fields = '__all__'
        
class TokenCreateForm(forms.ModelForm):
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