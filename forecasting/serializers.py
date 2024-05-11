from rest_framework import serializers
from django.utils import timezone

class DateField(serializers.ReadOnlyField):
    """
    A custom read-only field to convert datetime to date while preserving timezone information.
    """
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = timezone.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')  # Parse string to datetime
        return value.date()  # Convert datetime to date

class PurchaseDataSerializer(serializers.Serializer):
    
    drink_name = serializers.CharField(source='drink_rack__name')
    quantity = serializers.IntegerField(source='drink_quantity')
    date = DateField(source='purchase_rack__purchase__date_time')