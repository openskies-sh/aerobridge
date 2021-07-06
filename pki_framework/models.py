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
    
    KEY_ENVIRONMENT = ((0, _('OPERATOR')),(1, _('MANUFACTURER')),(2, _('PILOT')),(3, _('RFM')),(4, _('DSC / eMudra Token')),)
    
    TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('OTHER')),(4, _('DIGITAL_CERTIFICATE')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Enter a friendly name / description for the type of credential you are storing", validators = [no_special_characters_regex,])
    token_type = models.IntegerField(choices=TOKEN_TYPE, help_text="Set the type of credential this is, e.g Public / Private Key")
    association = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4, help_text="Set the entity this credential is associated with. The association will be used when calling Digital Sky and other external servers")
    token = models.BinaryField()

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