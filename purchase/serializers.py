from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from customer.models import Customer
from purchase.models import Purchase
from storehouse.models import Storehouse

class PurchaseSerializer(ModelSerializer):
    
    # N'afficher que les clients et dépôts non supprimés
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.filter(deleted_at=None))
    storehouse = serializers.PrimaryKeyRelatedField(queryset=Storehouse.objects.filter(deleted_at=None))
    
    class Meta:
        model = Purchase
        fields = ['id', 'date_time', 'customer', 'storehouse']