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
    
    def create(self, request, *args, **kwargs):
        # Vérifier si le contenu de la requête est JSON
        if request.content_type == 'application/json':
            # Analyser les données JSON envoyées dans la requête
            json_data = request.data
            
            # Extraire les données de l'objet JSON
            category_name = json_data.get('category_name')
            
            # Créer une nouvelle instance de catégorie
            category = Category.objects.create(name=category_name)
            
            # Serializer la nouvelle instance de catégorie
            serializer = CategorySerializer(category)
            
            # Retourner une réponse avec les données sérialisées
            return Response(serializer.data, status=201)
        else:
            # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
            return Response({'error': 'Invalid content type'}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)