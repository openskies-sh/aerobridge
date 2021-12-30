from rest_framework import serializers

from .models import DigitalSkyLog


class DigitalSkyLogSerializer(serializers.ModelSerializer):
    ''' A serializer for Digital Sky logs '''

    class Meta:
        model = DigitalSkyLog
        ordering = ['-created_at']
        exclude = ('created_at',)
