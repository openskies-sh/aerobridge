from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Authorization, Activity, Operator, Contact, Aircraft, Pilot
# Register your models here.

admin.site.register(Authorization)
admin.site.register(Activity)
admin.site.register(Operator)
admin.site.register(Contact)
admin.site.register(Pilot)
admin.site.register(Aircraft, SimpleHistoryAdmin)
