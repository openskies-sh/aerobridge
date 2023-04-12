from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from registry.models import Aircraft, Company, Operator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from common.validators import validate_currency_code, validate_url
no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$', message="No special characters allowed in this field.")


class AerobridgeCredential(models.Model):
    ''' A class to store different tokens used in drone operations '''
    
    KEY_ENVIRONMENT = ((0, _('Operator')),(1, _('Manufacturer')),(2, _('Pilot')),(3, _('RFM')),(4, _('Company')),(5, _('Management Server')),)
    TOKEN_TYPE= ((0, _('Public Key')),(1, _('x509 Digital Certificate')),(2, _('Other')),)
    FILE_EXTENSION = ((0, _('other')),(1, _('jwk')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100, help_text="Provide a friendly name / description for the type of credential you are storing e.g. eBee Public Key", validators = [no_special_characters_regex,])
    
    token_type = models.IntegerField(choices=TOKEN_TYPE, help_text="Set the type of credential this is, e.g Public / Private Key etc.")
    association = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4, help_text="Set the entity this credential is associated with. The association will be used when calling external servers.")
    token = models.BinaryField()
    
    extension = models.IntegerField(choices=FILE_EXTENSION, help_text="Specify the data format for this credential, if known", default = 0)

    aircraft = models.ForeignKey(Aircraft,blank=True, null=True, on_delete = models.CASCADE)
    manufacturer = models.ForeignKey(Company,blank=True, null=True, on_delete = models.CASCADE, limit_choices_to={'role':1})
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

      
class AerobridgeExternalCredential(models.Model):
    ''' A model for custom firmware '''
    KEY_ENVIRONMENT = ((0, _('Auth Server')),)
    TOKEN_TYPE= ((0, _('Full Chain')),)
    token_type = models.IntegerField(choices=TOKEN_TYPE, help_text="Set the type of credential this is, e.g Public / Private Key etc.")
    association = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4, help_text="Set the entity this credential is associated with. The association will be used when calling external servers.")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    binary_file_url = models.URLField(help_text="Enter a url from where the credential can be downloaded",validators=[validate_url])
    
    name = models.CharField(max_length=140, help_text="Give it a friendly name e.g. Auth server full chain pem")
    is_active = models.BooleanField(default=False,
                                    help_text="Set if the credential is active, don't forget to mark old credentials as inactive")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.version

    def __str__(self):
        return self.version
