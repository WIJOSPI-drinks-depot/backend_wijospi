from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from storehouse.models import Storehouse
from storehouse.models import StorehouseDrinkRack
from storehouse.serializers import StorehouseSerializer
from storehouse.serializers import StorehouseDrinkRackSerializer

class StorehouseViewset(ModelViewSet):
    
    serializer_class = StorehouseSerializer
    
    def get_queryset(self):
        queryset = Storehouse.objects.filter(deleted_at=None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class StorehouseDrinkRackViewset(ModelViewSet):
    
    serializer_class = StorehouseDrinkRackSerializer
    
    def get_queryset(self):
        queryset = StorehouseDrinkRack.objects.filter(deleted_at=None)
        
        return queryset
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
