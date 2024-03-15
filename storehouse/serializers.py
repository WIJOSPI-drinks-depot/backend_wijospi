from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from storehouse.models import Storehouse
from storehouse.models import StorehouseDrinkRack

class StorehouseSerializer(ModelSerializer):
    
    class Meta:
        model = Storehouse
        fields = ['id', 'name', 'contact', 'type', 'address', 'email', 'password', 'drink_racks']
        
class StorehouseDrinkRackSerializer(ModelSerializer):
    
    class Meta:
        model = StorehouseDrinkRack
        fields = ['id', 'storehouse', 'drink_rack', 'stock_quantity', 'creation_date']