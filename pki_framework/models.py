from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _
from registry.models import Aircraft, Manufacturer, Operator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$', message="No special characters allowed in this field.")


class AerobridgeCredential(models.Model):
    ''' A class to store tokens from Digital Sky '''
    
    KEY_ENVIRONMENT = ((0, _('Operator')),(1, _('Manufacturer')),(2, _('Pilot')),(3, _('RFM')),(4, _('Company')),(5, _('Management Server')),)
    TOKEN_TYPE= ((0, _('Public Key')),(1, _('Private Key')),(2, _('Authentication Token')),(3, _('Other')),(4, _('x509 Digital Certificate')),)
    FILE_EXTENSION = ((0, _('other')),(1, _('.der')),(2, _('.csr')),(3, _('.key')),(4, _('.cer')),(5, _('.pem'),))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Provide a friendly name / description for the type of credential you are storing e.g. eBee Public Key", validators = [no_special_characters_regex,])
    
    token_type = models.IntegerField(choices=TOKEN_TYPE, help_text="Set the type of credential this is, e.g Public / Private Key etc.")
    association = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4, help_text="Set the entity this credential is associated with. The association will be used when calling external servers.")
    token = models.BinaryField()
    
    extension = models.IntegerField(choices=FILE_EXTENSION, help_text="Specify the data format for this data, if known", default = 0)
    aircraft = models.ForeignKey(Aircraft,blank=True, null=True, on_delete = models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer,blank=True, null=True, on_delete = models.CASCADE)
    operator = models.ForeignKey(Operator,blank=True, null=True, on_delete = models.CASCADE)
    
    is_active = models.BooleanField(default = True, help_text="Set whether the credential is still active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        
        if (self.association == 0) and (self.operator is None):
            
            raise ValidationError('Please select a Operator for the Operator Token')
            
        elif self.association in [1] and self.manufacturer is None:
            raise ValidationError('Please select a Manufacturer for the Manufacturer Token')

        elif self.association in [3] and self.aircraft is None:
            raise ValidationError('Please select a Aircraft for the Aircraft Token')
    
    def token_type_verbose(self):
        return dict(AerobridgeCredential.TOKEN_TYPE)[self.token_type]