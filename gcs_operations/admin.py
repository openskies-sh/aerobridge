from django.contrib import admin
from .models import FlightPlan, FlightOperation, Transaction, FlightPermission, UINApplication
# Register your models here.

admin.site.register(FlightPlan)
admin.site.register(FlightOperation)
admin.site.register(Transaction)
admin.site.register(FlightPermission)
admin.site.register(UINApplication)
