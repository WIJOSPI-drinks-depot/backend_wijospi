from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from storehouse.models import Storehouse
from storehouse.models import StorehouseDrinkRack
from storehouse.serializers import StorehouseSerializer
from storehouse.serializers import StorehouseDrinkRackSerializer

# Messages types
error = 'error'
success = 'success'

class StorehouseViewset(ModelViewSet):
    
    serializer_class = StorehouseSerializer
    
    def get_queryset(self):
        queryset = Storehouse.objects.filter(deleted_at=None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                storehouse_name = json_data.get('name')
                storehouse_contact = json_data.get('contact')
                storehouse_type = json_data.get('type')
                storehouse_address = json_data.get('address')
                storehouse_email = json_data.get('email')
                storehouse_hashed_password = make_password(json_data.get('password'))
                
                storehouse = Storehouse.objects.create(
                    name = storehouse_name,
                    contact = storehouse_contact,
                    type = storehouse_type,
                    address = storehouse_address,
                    email = storehouse_email,
                    password = storehouse_hashed_password,
                )
                
                serializer = StorehouseSerializer(storehouse)
                
                return Response({'storehouse': serializer.data, 'message': 'Dépôt de boisson enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
            return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        # Vérifier si la méthode est PUT et le contenu de la requête est JSON
        if request.method == 'PUT' and request.content_type == 'application/json':
            try:
                instance = self.get_object()
                json_data = request.data
                
                storehouse_name = json_data.get('name')
                storehouse_contact = json_data.get('contact')
                storehouse_type = json_data.get('type')
                storehouse_address = json_data.get('address')
                storehouse_email = json_data.get('email')
                storehouse_hashed_password = make_password(json_data.get('password'))
                
                instance.name = storehouse_name
                instance.contact = storehouse_contact
                instance.type = storehouse_type
                instance.address = storehouse_address
                instance.email = storehouse_email
                instance.password = storehouse_hashed_password
                instance.save()
                
                serializer = StorehouseSerializer(instance)
                
                return Response({'storehouse': serializer.data, 'message': 'Dépôt de boisson modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
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

class StorehouseDrinkRackViewset(ModelViewSet):
    
    serializer_class = StorehouseDrinkRackSerializer
    
    def get_queryset(self):
        queryset = StorehouseDrinkRack.objects.filter(deleted_at=None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                storehouse_drink_rack_storehouse = json_data.get('storehouse')
                storehouse_drink_rack_drink_rack = json_data.get('drink_rack')
                storehouse_drink_rack_stock_quantity = json_data.get('stock_quantity')
                storehouse_drink_rack_creation_date = json_data.get('creation_date')
                
                storehouse = Storehouse.objects.create(
                    storehouse = storehouse_drink_rack_storehouse,
                    drink_rack = storehouse_drink_rack_drink_rack,
                    stock_quantity = storehouse_drink_rack_stock_quantity,
                    creation_date = storehouse_drink_rack_creation_date,
                )
                
                serializer = StorehouseSerializer(storehouse)
                
                return Response({'storehouse': serializer.data, 'message': 'Quantité de stock enregistrée avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                error_message = e.messages
                
                return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
            return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        # Vérifier si la méthode est PUT et le contenu de la requête est JSON
        if request.method == 'PUT' and request.content_type == 'application/json':
            try:
                instance = self.get_object()
                json_data = request.data
                
                storehouse_drink_rack_storehouse = json_data.get('storehouse')
                storehouse_drink_rack_drink_rack = json_data.get('drink_rack')
                storehouse_drink_rack_stock_quantity = json_data.get('stock_quantity')
                storehouse_drink_rack_creation_date = json_data.get('creation_date')
                
                instance.storehouse = storehouse_drink_rack_storehouse
                instance.drink_rack = storehouse_drink_rack_drink_rack
                instance.stock_quantity = storehouse_drink_rack_stock_quantity
                instance.creation_date = storehouse_drink_rack_creation_date
                instance.save()
                
                serializer = StorehouseSerializer(instance)
                
                return Response({'storehouse_drink_rack': serializer.data, 'message': 'Quantité de stock modifiée avec succès.', 'type': success}, status=status.HTTP_200_OK)
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
