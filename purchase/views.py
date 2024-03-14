from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from purchase.models import Purchase
from purchase.serializers import PurchaseSerializer

class PurchaseViewset(ModelViewSet):
    
    serializer_class = PurchaseSerializer
    
    def get_queryset(self):
        queryset = Purchase.objects.filter(deleted_at = None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
