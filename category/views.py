from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from category.models import Category
from category.serializers import CategorySerializer

class CategoryViewset(ModelViewSet):
    
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        queryset = Category.objects.filter(deleted_at=None)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)