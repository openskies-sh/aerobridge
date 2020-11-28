from rest_framework import serializers
from .models import Transaction



class TransactionSerializer(serializers.ModelSerializer):
    ''' A serializer to the transaction view '''

    class Meta:
        model = Transaction		
        ordering = ['-created_at']
