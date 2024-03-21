from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from storehouse.models import Storehouse
from supply.models import Supply
from supply.models import SupplyDrinkRack

class SupplySerializer(ModelSerializer):
    
    # Afficher uniquement les dépôts non supprimés
    storehouse = serializers.PrimaryKeyRelatedField(queryset=Storehouse.objects.filter(deleted_at=None))
    
    class Meta:
        model = Supply
        fields = ['id', 'date', 'storehouse', 'drink_racks']
        
class SupplyDrinkRackSerializer(ModelSerializer):
    
    class Meta:
        model = SupplyDrinkRack
        fields = ['id', 'supply', 'drink_rack', 'supply_quantity']