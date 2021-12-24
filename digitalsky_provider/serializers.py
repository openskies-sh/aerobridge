from rest_framework import serializers

from .models import DigitalSkyLog


# Enabling it only for the unit tests, would still be disabled at the API level
class DigitalSkyLogSerializer(serializers.ModelSerializer):
    ''' A serializer to the drone create view '''

    class Meta:
        model = DigitalSkyLog
        ordering = ['-created_at']
        exclude = ('created_at',)
