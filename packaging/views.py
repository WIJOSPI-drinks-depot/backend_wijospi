from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from packaging.models import Packaging
from packaging.serializers import PackagingSerializer

class PackagingViewset(ModelViewSet):
    
    serializer_class = PackagingSerializer
    
    def get_queryset(self):
        queryset = Packaging.objects.filter(deleted_at = None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
