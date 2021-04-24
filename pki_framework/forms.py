from .models import DigitalSkyCredentials
from django.forms import ModelForm, widgets
from django import forms
from django.utils.translation import ugettext_lazy as _

TOKEN_TYPE= ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DRONE')),)

class TokenCreateForm(ModelForm):
    class Meta:
        model = DigitalSkyCredentials
        fields = '__all__'
        
class CutsomTokenCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    token_type = forms.IntegerField(widget=forms.Select(choices=TOKEN_TYPE),
    )
    token = forms.CharField(widget = forms.TextInput())