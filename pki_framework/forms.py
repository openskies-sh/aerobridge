from .models import AerobridgeCredential
from django.forms import ModelForm, widgets
from django import forms
from django.utils.translation import ugettext_lazy as _


KEY_ENVIRONMENT = ((0, _('OPERATOR')),(1, _('MANUFACTURER')),(2, _('PILOT')),(3, _('RFM')),(4, _('DSC / eMudra Token')),)
    
TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('OTHER')),(4, _('DIGITAL_CERTIFICATE')),)
    
class TokenCreateForm(ModelForm):    
    token = forms.CharField(widget = forms.TextInput())

    class Meta:
        model = AerobridgeCredential
        fields = "__all__" 
        
        
class CutsomTokenCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    token_type = forms.IntegerField(widget=forms.Select(choices=TOKEN_TYPE),)
    environment = forms.IntegerField(widget=forms.Select(choices=KEY_ENVIRONMENT),)
    token = forms.CharField(widget = forms.TextInput())

