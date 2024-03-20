from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from packaging.models import Packaging
from packaging.serializers import PackagingSerializer

# Messages types
error = 'error'
success = 'success'

class PackagingViewset(ModelViewSet):
    
    serializer_class = PackagingSerializer
    
    def get_queryset(self):
        queryset = Packaging.objects.filter(deleted_at = None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                packaging_name = json_data.get('packaging_name')
                
                packaging = Packaging.objects.create(name=packaging_name)
                
                serializer = PackagingSerializer(packaging)
                
                return Response({'packaging': serializer.data, 'message': 'Conditionnement enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
        return
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
