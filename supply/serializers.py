from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from storehouse.models import Storehouse
from supply.models import Supply

class SupplySerializer(ModelSerializer):
    
    # Afficher uniquement les dépôts non supprimés
    storehouse = serializers.PrimaryKeyRelatedField(queryset=Storehouse.objects.filter(deleted_at=None))
    
    class Meta:
        model = Supply
        fields = ['id', 'date', 'storehouse', 'drink_racks']