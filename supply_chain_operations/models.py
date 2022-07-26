from django.db import models
import uuid
from registry.models import Aircraft, AircraftComponent
from gcs_operations.models import FlightLog
from django.utils.translation import gettext_lazy as _
from common.status_codes import StockStatus
from django.core.validators import MinValueValidator
class Incident(models.Model):
    
    """
    A object to hold details of an incident around aircraft
    """  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.CASCADE,
        verbose_name=_('Impacted Aicraft'),
        help_text=_('Select the aircraft assocated with this event')        
    )
    flight_log = models.ForeignKey(FlightLog, on_delete=models.CASCADE,null=True,blank=True,  help_text=_("Associate a Flight Log with this incident"))
    impacted_components = models.ManyToManyField(AircraftComponent,  help_text=_("Associate the components associated with this event with this incident"))
    notes = models.TextField(help_text="Describe the event in detail")
    new_status = models.PositiveIntegerField(
        default=StockStatus.UNAVAILABLE_CODES,
        choices=StockStatus.items(),
        validators=[MinValueValidator(0)])


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.aircraft + ' ' + self.notes[:10]  + '..'

    def __str__(self):
        return self.aircraft + ' ' + self.notes[:10] + '..'
