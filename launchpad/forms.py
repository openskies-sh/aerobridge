from registry.models import Person, Address, Operator, Aircraft, Manufacturer, Firmware, Contact, Pilot
from digitalsky_provider.models import DigitalSkyLog
from gcs_operations.models import FlightOperation, FlightLog, FlightPlan, FlightPermission, Transaction
from django import forms
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
        exclude = ('is_registered','type_certificate','esn',)

class ManufacturerCreateForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FirmwareCreateForm(forms.ModelForm):
    class Meta:
        model = Firmware
        fields = '__all__'

class FlightPlanCreateForm(forms.ModelForm):
    class Meta:
        model = FlightPlan
        fields = '__all__'

class FlightPermissionCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    super(FlightPermissionCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['is_successful'].widget.attrs['disabled'] = True
    #    self.fields['artefact'].widget.attrs['disabled'] = True

    class Meta:
        model = FlightPermission
        fields = ('operation',)
        

class FlightLogCreateForm(forms.ModelForm):
    class Meta:
        model = FlightLog
        fields = ('operation','raw_log', 'signed_log',)
        

class FlightOperationCreateForm(forms.ModelForm):
    class Meta:
        model = FlightOperation
        fields = '__all__'


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
