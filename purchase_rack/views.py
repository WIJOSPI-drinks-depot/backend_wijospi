from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from purchase_rack.models import PurchaseRack
from purchase_rack.serializers import PurchaseRackSerializer

class PurchaseRackViewset(ModelViewSet):
    
    serializer_class = PurchaseRackSerializer
    
    def get_queryset(self):
        queryset = PurchaseRack.objects.filter(deleted_at = None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
