from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import AircraftMasterComponent, AircraftModel, Authorization, Activity, Company, Operator, Contact, Aircraft, Pilot, AircraftDetail, AircraftComponent,AircraftComponentSignature, Firmware, AircraftAssembly
# Register your models here.

admin.site.register(Authorization)
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Firmware)
admin.site.register(Operator)
admin.site.register(Contact)
admin.site.register(Pilot)
admin.site.register(Aircraft, SimpleHistoryAdmin)
admin.site.register(AircraftModel,SimpleHistoryAdmin)
admin.site.register(AircraftAssembly,SimpleHistoryAdmin)
admin.site.register(AircraftDetail, SimpleHistoryAdmin)
admin.site.register(AircraftMasterComponent, SimpleHistoryAdmin)
admin.site.register(AircraftComponent, SimpleHistoryAdmin)
admin.site.register(AircraftComponentSignature, SimpleHistoryAdmin)
