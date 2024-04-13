from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drink_rack.models import DrinkRack
from category.models import Category
from packaging.models import Packaging
from drink_rack.serializers import DrinkRackSerializer

# Messages types
error = 'error'
success = 'success'

class DrinkRackViewset(ModelViewSet):
    
    serializer_class = DrinkRackSerializer
    
    def get_queryset(self):
        queryset = DrinkRack.objects.filter(deleted_at = None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                drink_rack_name = json_data.get('name')
                drink_rack_capacity = json_data.get('capacity')
                drink_rack_lifespan = json_data.get('lifespan')
                drink_rack_price = json_data.get('price')
                drink_rack_category = json_data.get('category')
                drink_rack_packaging = json_data.get('packaging')
                
                drink_rack = DrinkRack.objects.create(
                    name = drink_rack_name,
                    capacity = drink_rack_capacity,
                    lifespan = drink_rack_lifespan,
                    price = drink_rack_price,
                    category = Category.objects.get(id = drink_rack_category),
                    packaging = Packaging.objects.get(id = drink_rack_packaging)
                )
                
                serializer = DrinkRackSerializer(drink_rack)
                
                return Response({'drink_rack': serializer.data, 'message': 'Casier de boisson enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
            
    def update(self, request, *args, **kwargs):
        # Vérifier si la méthode est PUT et le contenu de la requête est JSON
        if request.method == 'PUT' and request.content_type == 'application/json':
            try:
                instance = self.get_object()
                json_data = request.data
                
                drink_rack_name = json_data.get('name')
                drink_rack_capacity = json_data.get('capacity')
                drink_rack_lifespan = json_data.get('lifespan')
                drink_rack_price = json_data.get('price')
                drink_rack_category = json_data.get('category')
                drink_rack_packaging = json_data.get('packaging')
                
                instance.name = drink_rack_name
                instance.capacity = drink_rack_capacity
                instance.lifespan = drink_rack_lifespan
                instance.price = drink_rack_price
                instance.category = Category.objects.get(id = drink_rack_category)
                instance.packaging = Packaging.objects.get(id = drink_rack_packaging)
                instance.save()
                
                serializer = DrinkRackSerializer(instance)
                
                return Response({'drink_rack': serializer.data, 'message': 'Casier de boisson modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
