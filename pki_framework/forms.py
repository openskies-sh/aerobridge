from .models import DigitalSkyCredentials
from django.forms import ModelForm

class TokenCreateForm(ModelForm):
    class Meta:
        model = DigitalSkyCredentials
        fields = '__all__'
        