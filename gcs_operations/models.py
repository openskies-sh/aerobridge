from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _
import string, random 
import os, random, string
from django.utils import timezone as tz
from registry.models import Aircraft, Operator,Activity

def make_random_plan_common_name(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Create your models here.
class FlightPlan(models.Model):
    ''' This is a model to hold flight plan in a GeoJSON format '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default= 'Flight Plan ' + make_random_plan_common_name(6))
    details = models.TextField(null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
       return self.name

    def __str__(self):
        return self.name 


    
class FlightOperation(models.Model):
    ''' A flight operation object for NPNT permission ''' 
    OPERATION_TYPES = ((0, _('VLOS')),(1, _('BVLOS')),)
    
    name = models.CharField(max_length=20, default= 'Flight Operation ' + make_random_plan_common_name(6))
    drone = models.ForeignKey(Aircraft,models.CASCADE)
    flight_plan = models.ForeignKey(FlightPlan,models.CASCADE)
    purpose = models.ForeignKey(Activity, models.CASCADE, default= '7a875ff9-79ee-460e-816f-30360e0ac645', help_text="To add additional categories, please add entries to the Activities table")
    type_of_operation = models.IntegerField(choices=OPERATION_TYPES, default=0, help_text="At the moment, only VLOS and BVLOS operations are supported, for other types of operations, please issue a pull-request")
    flight_termination_or_return_home_capability = models.BooleanField(default =1)
    geo_fencing_capability = models.BooleanField(default =1)
    detect_and_avoid_capability= models.BooleanField(default =0)
    recurring_time_expression = models.CharField(max_length=50, default = "0 0 0 ? * 1#1 *")
    recurring_time_duration = models.IntegerField(default=60)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
       return self.name + ' ' + self.flight_plan.name

    def __str__(self):
        return self.name + ' ' + self.flight_plan.name



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
    is_successful = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
       return self.operation.name

    def __str__(self):
        return self.operation.name


    
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
    
    def __unicode__(self):
       return self.id

    def __str__(self):
        return self.id

