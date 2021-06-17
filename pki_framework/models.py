from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _
from registry.models import Aircraft, Contact

class AerobridgeCredential(models.Model):
    ''' A class to store tokens from Digital Sky '''
    
    KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('DSC / eMudra Token')),)
    
    TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('OTHER')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Enter a friendly name / description for the type of credential you are storing")
    token_type = models.IntegerField(choices=TOKEN_TYPE, help_text="Set the type of credential this is")
    association = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4, help_text="Set the entity this credential is associated with. The association will be used when calling Digital Sky and other external servers")
    token = models.BinaryField()
    
    is_active = models.BooleanField(default = True, help_text="Set whether the credential is still active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def token_type_verbose(self):
        return dict(AerobridgeCredential.TOKEN_TYPE)[self.token_type]