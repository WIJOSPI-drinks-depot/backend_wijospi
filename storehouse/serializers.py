from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from storehouse.models import Storehouse

class StorehouseSerializer(ModelSerializer):
    
    class Meta:
        model = Storehouse
        fields = ['id', 'name', 'contact', 'type', 'address', 'email', 'password', 'drink_racks']