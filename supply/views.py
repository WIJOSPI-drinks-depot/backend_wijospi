from dateutil import parser
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drink_rack.models import DrinkRack
from storehouse.models import Storehouse
from supply.models import Supply
# from supply.models import SupplyDrinkRack # Si on veut ajouter plusieurs boissons à un même approvisionnement
from supply.serializers import SupplySerializer

# Messages types
error = 'error'
success = 'success'

class SupplyViewset(ModelViewSet):
    
    serializer_class = SupplySerializer
    
    def get_queryset(self):
        queryset = Supply.objects.filter(deleted_at=None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                supply_date_time_string = json_data.get('date_time')
                supply_date_time = parser.parse(supply_date_time_string)
                supply_date_time_formatted = supply_date_time.strftime("%Y-%m-%d %H:%M:%S")
                supply_storehouse = json_data.get('storehouse')
                supply_drink_rack = json_data.get('drink_rack')
                supply_quantity = json_data.get('quantity')
                
                supply = Supply.objects.create(
                    date_time = supply_date_time_formatted,
                    storehouse = Storehouse.objects.get(id = supply_storehouse),
                    drink_rack = DrinkRack.objects.get(id = supply_drink_rack),
                    quantity = supply_quantity,
                )
                
                serializer = SupplySerializer(supply)
                
                return Response({'supply': serializer.data, 'message': 'Approvisionnement enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
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
                
                supply_date_time_string = json_data.get('date_time')
                supply_date_time = parser.parse(supply_date_time_string)
                supply_date_time_formatted = supply_date_time.strftime("%Y-%m-%d %H:%M:%S")
                supply_storehouse = json_data.get('storehouse')
                supply_drink_rack = json_data.get('drink_rack')
                supply_quantity = json_data.get('quantity')
                
                instance.date_time = supply_date_time_formatted
                instance.storehouse = Storehouse.objects.get(id = supply_storehouse),
                instance.drink_rack = DrinkRack.objects.get(id = supply_drink_rack),
                instance.quantity = supply_quantity
                instance.save()
                
                serializer = SupplySerializer(instance)
                
                return Response({'supply': serializer.data, 'message': 'Approvisionnement modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
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

# # Si on veut ajouter plusieurs boissons à un même approvisionnement
# class SupplyDrinkRackViewset(ModelViewSet):
    
#     serializer_class = SupplyDrinkRackSerializer
    
#     def get_queryset(self):
#         queryset = SupplyDrinkRack.objects.all()
        
#         return queryset
    
#     def create(self, request, *args, **kwargs):
#         # Vérifier si la méthode est POST et le contenu de la requête est JSON
#         if request.method == 'POST' and request.content_type == 'application/json':
#             try:
#                 json_data = request.data
                
#                 supply_drink_rack_supply = json_data.get('supply')
#                 supply_drink_rack_drink_rack = json_data.get('drink_rack')
#                 supply_drink_rack_supply_quantity = json_data.get('supply_quantity')
                
#                 supply_drink_rack = SupplyDrinkRack.objects.create(
#                     supply = supply_drink_rack_supply,
#                     drink_rack = supply_drink_rack_drink_rack,
#                     supply_quantity = supply_drink_rack_supply_quantity,
#                 )
                
#                 serializer = SupplyDrinkRackSerializer(supply_drink_rack)
                
#                 return Response({'supply_drink_rack': serializer.data, 'message': 'Quantité approvisionnée avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
#             except ValidationError as e:
#                 error_message = e.messages
                
#                 return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
#             return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
        
#     def update(self, request, *args, **kwargs):
#         # Vérifier si la méthode est PUT et le contenu de la requête est JSON
#         if request.method == 'PUT' and request.content_type == 'application/json':
#             try:
#                 instance = self.get_object()
#                 json_data = request.data
                
#                 supply_drink_rack_supply = json_data.get('supply')
#                 supply_drink_rack_drink_rack = json_data.get('drink_rack')
#                 supply_drink_rack_supply_quantity = json_data.get('supply_quantity')
                
#                 instance.supply = supply_drink_rack_supply
#                 instance.drink_rack = supply_drink_rack_drink_rack
#                 instance.supply_quantity = supply_drink_rack_supply_quantity
#                 instance.save()
            
#                 serializer = SupplyDrinkRackSerializer(instance)
                
#                 return Response({'supply_drink_rack': serializer.data, 'message': 'Quantité approvisionnée modifiée avec succès.', 'type': success}, status=status.HTTP_200_OK)
#             except ValidationError as e:
#                 error_message = e.messages
                
#                 return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
#             return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
    