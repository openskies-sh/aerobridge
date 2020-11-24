from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _
import string, random 
import os
from django.utils import timezone as tz

# Create your models here.

# Use camel case DGCA API required Snake Case
class Drone(models.Model):
    DRONE_TYPES = ((0, _('Quadcopter')),(1, _('Fixed Wing')))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_id = models.IntegerField(default=0, choices=DRONE_TYPES)
    version = models.CharField(max_length=5)
    device_id = models.CharField(max_length=64)
    device_model_id = models.CharField(max_length=64)
    operator_business_id = models.CharField(max_length=36, default=os.environ.get("OPERATOR_BUSINESS_ID"))
    is_registered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional ID Hash (See: https://digitalsky.dgca.gov.in/api-documentation)
    # id_hash = models.CharField(max_length=36)



class Transaction(models.Model):
    ''' This model provides a view of all transactions in the system ''' 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prefix = models.CharField(max_length=12, default = "")
    drone = models.ForeignKey(Drone, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_txn_id(self):
        transaction_prefix = self.prefix if (self.prefix.length > 0 ) else "default_txn"
        txn_id = transaction_prefix +"_" +str(self.id) 
        return txn_id