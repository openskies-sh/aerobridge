
from rest_framework import serializers
from supply_chain_operations.models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

