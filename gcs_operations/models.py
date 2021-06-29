from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
import string, random 
import os, random, string
from registry.models import Aircraft, Operator,Activity

def make_random_plan_common_name():
    length = 6
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Create your models here.
class FlightPlan(models.Model):
    ''' This is a model to hold flight plan in a GeoJSON format '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, default=  "Delivery Plan", help_text="Give this flight plan a friendly name")
    geo_json = models.TextField(help_text="Paste flight plan geometry as GeoJSON", default='{"type":"FeatureCollection","features":[]}')
    
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(default=datetime.now)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.name

    def __str__(self):
        return self.name 

    
class FlightOperation(models.Model):
    ''' A flight operation object for NPNT permission ''' 
    OPERATION_TYPES = ((0, _('VLOS')),(1, _('BVLOS')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, default="Medicine Delivery Operation", help_text="Give a friendly name for this operation")
    drone = models.ForeignKey(Aircraft, models.CASCADE)
    flight_plan = models.ForeignKey(FlightPlan, models.CASCADE)
    purpose = models.ForeignKey(Activity, models.CASCADE, default= '7a875ff9-79ee-460e-816f-30360e0ac645', help_text="To add additional categories, please add entries to the Activities table")
    type_of_operation = models.IntegerField(choices=OPERATION_TYPES, default=0, help_text="At the moment, only VLOS and BVLOS operations are supported, for other types of operations, please issue a pull-request")

    
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
        transaction_prefix = self.prefix if (len(self.prefix) > 0 ) else "default_txn"
        txn_id = transaction_prefix +"_" +str(self.id) 
        return txn_id
    
class FlightPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.ForeignKey(FlightOperation, models.CASCADE,related_name='Operation', null=True)
    is_successful = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    artefact = models.TextField(default="", help_text="If the text above is empty, permission artefact for this operation has not been received")
    
    def __unicode__(self):
       return self.operation.name

    def __str__(self):
        return self.operation.name

class FlightLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.ForeignKey(FlightOperation, on_delete=models.CASCADE)
    signed_log = models.URLField(help_text="Enter the URL of the Zip file that has the signed log.")
    raw_log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(default=False)
    
    
    def __unicode__(self):
       return self.operation.name

    def __str__(self):
        return self.operation.name
    

class CloudFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.URLField(help_text="URL location of the file")
    name = models.CharField(max_length=140, default="Uploaded File", help_text="Give name to this file e.g. Flight Log from Operation A on 21st Aug.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)