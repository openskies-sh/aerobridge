
from rest_framework import serializers
from supply_chain_operations.models import Incident
from registry.models import Aircraft

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
class IncidentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ("flight_log", "notes", "new_status")

