from django.db import models
from django_cryptography.fields import encrypt
import uuid

class DigitalSkyCredentials(models.Model):
    ''' A class to store tokens from Digital Sky '''
    
    DIGITAL_SKY_TOKEN_TYPE= ((0, _('OPERATOR')),(1, _('MANUFACTURER')),(2, _('Densely Populated')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    token_type = models.IntegerField(choices=DIGITAL_SKY_TOKEN_TYPE)
    token = models.BinaryField()
