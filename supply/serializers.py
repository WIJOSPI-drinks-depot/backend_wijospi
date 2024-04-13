from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from drink_rack.models import DrinkRack
from storehouse.models import Storehouse
from supply.models import Supply

class SupplySerializer(ModelSerializer):
    
    # Afficher uniquement les dépôts non supprimés
    storehouse = serializers.PrimaryKeyRelatedField(queryset=Storehouse.objects.filter(deleted_at=None))
    
    # Afficher uniquement les casiers de boisson non supprimés
    drink_rack = serializers.PrimaryKeyRelatedField(queryset=DrinkRack.objects.filter(deleted_at=None))
    
    class Meta:
        model = Supply
        fields = ['id', 'date_time', 'storehouse', 'drink_rack', 'quantity']