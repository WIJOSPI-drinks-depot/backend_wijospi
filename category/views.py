from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from category.models import Category
from category.serializers import CategorySerializer

# Messages types
error = 'error'
success = 'success'

class CategoryViewset(ModelViewSet):
    
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        queryset = Category.objects.filter(deleted_at=None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                category_name = json_data.get('category_name')
                
                category = Category.objects.create(name=category_name)
                
                serializer = CategorySerializer(category)
                
                return Response({'category': serializer.data, 'message': 'Catégorie enregistrée avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
            return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)