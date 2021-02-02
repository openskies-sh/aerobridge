from registry.models import Person, Address
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