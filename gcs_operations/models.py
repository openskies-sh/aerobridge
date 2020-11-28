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
from registry.models import Aircraft
# Create your models here.


class Transaction(models.Model):
    ''' This model provides a view of all transactions in the system ''' 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prefix = models.CharField(max_length=12, default = "")
    aircraft = models.ForeignKey(Aircraft, models.CASCADE,related_name='Aircraft', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_txn_id(self):
        transaction_prefix = self.prefix if (self.prefix.length > 0 ) else "default_txn"
        txn_id = transaction_prefix +"_" +str(self.id) 
        return txn_id