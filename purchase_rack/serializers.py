from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from purchase.models import Purchase
from purchase_rack.models import PurchaseRack

class PurchaseRackSerializer(ModelSerializer):
    
    # N'afficher que les achats non supprimés
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.filter(deleted_at=None))
    
    class Meta:
        model = PurchaseRack
        fields = ['id', 'capacity', 'quantity', 'purchase']
        # read_only_fields = ['capacity']