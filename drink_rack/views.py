from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drink_rack.models import DrinkRack
from drink_rack.serializers import DrinkRackSerializer

class DrinkRackViewset(ModelViewSet):
    
    serializer_class = DrinkRackSerializer
    
    def get_queryset(self):
        queryset = DrinkRack.objects.filter(deleted_at = None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
