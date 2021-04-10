from django.db import models
import uuid
from django.utils.translation import ugettext_lazy as _

class DigitalSkyCredentials(models.Model):
    ''' A class to store tokens from Digital Sky '''
    
    TOKEN_TYPE= ((0, _('DIGITAL_SKY_OPERATOR')),(1, _('DIGITAL_SKY_MANUFACTURER')),(2, _('DRONE')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    token_type = models.IntegerField(choices=TOKEN_TYPE)
    token = models.BinaryField()
