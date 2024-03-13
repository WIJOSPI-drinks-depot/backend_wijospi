from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from packaging.models import Packaging

class PackagingSerializer(ModelSerializer):
    
    class Meta:
        model = Packaging
        fields = ['id', 'name']