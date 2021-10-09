from django.db import models

# Create your models here.
import uuid
from gcs_operations.models import Transaction
# Create your models here.

# Use camel case DGCA API required Snake Case
class DigitalSkyLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    txn = models.ForeignKey(Transaction,  models.CASCADE)
    response_code = models.CharField(max_length=256)
    response = models.TextField(default="Raw response from DGCA Digital Sky Server is stored here.")
    timestamp = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    