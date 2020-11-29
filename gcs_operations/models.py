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
from registry.models import Aircraft, Operator


# Create your models here.
class FlightPlan(models.Model):
    ''' This is a model to hold flight plan in a GeoJSON format '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    details = models.TextField(null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class FlightOperation(models.Model):
    ''' A flight operation object for NPNT permission ''' 
    drone = models.ForeignKey(Aircraft,models.CASCADE)
    flight_plan = models.ForeignKey(FlightPlan,models.CASCADE)
    purpose = models.CharField(max_length=140)
    type_of_operation = models.CharField(max_length=140)
    flight_termination_or_return_home_capability = models.BooleanField(default =1)
    geo_fencing_capability = models.BooleanField(default =1)
    detect_and_avoid_capability= models.BooleanField(default =0)
    recurring_time_expression = models.CharField(max_length=50, default = "0 0 0 ? * 1#1 *")
    recurring_time_duration = models.IntegerField(default=60)
    
    created_at = models.DateTimeField(auto_now_add=True)

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
    
class FlightPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.ForeignKey(FlightOperation, models.CASCADE,related_name='Operation', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class UINApplication(models.Model):
    ''' This is the UIN application object '''
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fee_details = models.CharField(max_length=140)
    drone = models.ForeignKey(Aircraft,models.CASCADE)
    operator = models.ForeignKey(Operator,models.CASCADE)
    import_permission = models.URLField()
    cin = models.URLField()
    gst_in = models.URLField()
    pan_card = models.URLField()
    dot_permission = models.URLField()
    security_clearance = models.URLField()
    eta = models.URLField()
    op_manual = models.URLField()
    maintainence_guidelines = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    