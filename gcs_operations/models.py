from django.db import models
import uuid

# Create your models here.
from django.utils import timezone as tz
from django.utils.translation import gettext_lazy as _
import string, random 
import os, random, string
from registry.models import Aircraft,Activity, Operator, Pilot
from django.core.validators import RegexValidator


no_special_characters_regex = RegexValidator(regex=r'^[-, ,_\w]*$', message="No special characters allowed in this field.")

class FlightPlan(models.Model):
    ''' This is a model to hold flight plan in a GeoJSON format '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140, default=  "Delivery Plan", help_text="Give this flight plan a friendly name")    
    plan_file_json = models.JSONField(help_text = "Paste the QGCS flight plan JSON, for more information about the Plan File Format see: https://dev.qgroundcontrol.com/master/en/file_formats/plan.html", default = dict)
    geo_json = models.JSONField(default=dict, help_text="Paste the flight plan as GeoJSON")
    is_editable = models.BooleanField(default=True, help_text="Set whether the flight plan can be edited. Once the flight log has been signed a flight plan cannot be edited.")
    
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
    drone = models.ForeignKey(Aircraft, models.CASCADE, help_text="Pick the drone that will be used to fly this opreation")
    flight_plan = models.ForeignKey(FlightPlan, models.CASCADE, help_text="Pick a flight plan for this operation")
    operator = models.ForeignKey(Operator, models.CASCADE, help_text="Assign a operator for this operaiton")
    purpose = models.ForeignKey(Activity, models.CASCADE, default= '7a875ff9-79ee-460e-816f-30360e0ac645', help_text="To add additional categories, please add entries to the Activities table")
    type_of_operation = models.IntegerField(choices=OPERATION_TYPES, default=0, help_text="At the moment, only VLOS and BVLOS operations are supported, for other types of operations, please issue a pull-request")
    pilot = models.ForeignKey(Pilot, models.CASCADE)
    is_editable = models.BooleanField(default=True, help_text="Set whether the flight operation can be edited. Once the flight log has been signed a flight operation cannot be edited.")
    
    start_datetime = models.DateTimeField(default= tz.now, help_text="Specify Flight start date and time in Indian Standard Time (IST)")
    end_datetime = models.DateTimeField(default=tz.now, help_text="Specify Flight end date and time in Indian Standard Time (IST)")
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
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
    GRANTED = 'granted'
    DENIED = 'denied'
    PENDING = 'pending'
    
    PERMISSION_STATUS_CHOICES = [
        (GRANTED, 'granted'),
        (DENIED, 'denied'),        
        (PENDING, 'pending'),  
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.OneToOneField(FlightOperation, models.CASCADE,related_name='Operation')    
    token = models.JSONField(default=dict)   
    geo_cage = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status_code = models.CharField(
        max_length=20,
        choices=PERMISSION_STATUS_CHOICES,
        default=DENIED, help_text="Permissions")
    
    def __unicode__(self):
       return self.operation.name

    def __str__(self):
        return self.operation.name


class FlightLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation = models.ForeignKey(FlightOperation, on_delete=models.CASCADE)    
    raw_log = models.JSONField(default= dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True, help_text="Set whether the flight log can be edited. Once the flight log has been signed raw flight log cannot be edited.")

    def __unicode__(self):
       return self.operation.name

    def __str__(self):
        return self.operation.name
    
class SignedFlightLog(models.Model):
    ''' As of August 2021, it is unclear if the flight logs will be signed by the GCS or if the flight log will be signed by the management server. By sepearating the flight log and signed flight log we enable either cases. '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raw_flight_log = models.OneToOneField(FlightLog, on_delete=models.CASCADE, related_name ="raw_flight_log")
    signed_log = models.TextField(help_text="Flight log signed by the drone private key")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.raw_flight_log.operation.name

    def __str__(self):
        return self.raw_flight_log.operation.name
    

class CloudFile(models.Model):
    UPLOAD_TYPE = (
        ('logs', 'Logs'),
        ('documents', 'Documents'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.URLField(help_text="URL location of the file")
    name = models.CharField(max_length=140, default="Uploaded File", help_text="Give name to this file e.g. Flight Log from Operation A on 21st Aug.")
    upload_type = models.CharField(max_length=20,choices=UPLOAD_TYPE,default='other')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)