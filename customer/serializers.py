from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from customer.models import Customer

class CustomerSerializer(ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'surname', 'contact', 'address', 'email', 'password']