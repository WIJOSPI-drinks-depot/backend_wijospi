from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from category.models import Category
from drink_rack.models import DrinkRack
from packaging.models import Packaging

class DrinkRackSerializer(ModelSerializer):
    
    # Afficher uniquement les catégories et conditionnements non supprimés
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(deleted_at=None))
    packaging = serializers.PrimaryKeyRelatedField(queryset=Packaging.objects.filter(deleted_at=None))
    
    class Meta:
        model = DrinkRack
        fields = ['id', 'name', 'capacity', 'lifespan', 'price', 'category', 'packaging']