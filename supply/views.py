from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from supply.models import Supply
from supply.serializers import SupplySerializer

class SupplyViewset(ModelViewSet):
    
    serializer_class = SupplySerializer
    
    def get_queryset(self):
        queryset = Supply.objects.filter(deleted_at=None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)