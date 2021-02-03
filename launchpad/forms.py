from registry.models import Person, Address, Operator, Aircraft
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
