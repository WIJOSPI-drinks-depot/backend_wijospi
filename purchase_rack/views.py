
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drink_rack.models import DrinkRack
from purchase.models import Purchase
from purchase_rack.models import PurchaseRack
from purchase_rack.models import PurchaseRackDrinkRack
from purchase_rack.serializers import PurchaseRackSerializer
from purchase_rack.serializers import PurchaseRackDrinkRackSerializer

# Messages types
error = 'error'
success = 'success'

class PurchaseRackViewset(ModelViewSet):
    
    serializer_class = PurchaseRackSerializer
    
    def get_queryset(self):
        queryset = PurchaseRack.objects.filter(deleted_at = None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                purchase_rack_capacity = json_data.get('capacity')
                purchase_rack_quantity = json_data.get('quantity')
                purchase_rack_purchase_id = json_data.get('purchase')
                purchase_rack_purchase = Purchase.objects.get(id = purchase_rack_purchase_id)
                
                # Créer le casier d'achat
                purchase_rack = PurchaseRack.objects.create(
                    capacity = purchase_rack_capacity,
                    quantity = purchase_rack_quantity,
                    purchase = purchase_rack_purchase,
                )
                
                purchase_rack_serializer = PurchaseRackSerializer(purchase_rack)

                # Définir le nombre de ce casier à acheter
                purchase_rack_drink_rack_purchase_rack = purchase_rack
                purchase_rack_drink_rack_drink_rack_id = json_data.get('drink_rack')
                purchase_rack_drink_rack_drink_rack = DrinkRack.objects.get(id = purchase_rack_drink_rack_drink_rack_id)
                purchase_rack_drink_rack_drink_quantity = json_data.get('drink_quantity')
                
                purchase_rack_drink_rack = PurchaseRackDrinkRack.objects.create(
                    purchase_rack = purchase_rack_drink_rack_purchase_rack,
                    drink_rack = purchase_rack_drink_rack_drink_rack,
                    drink_quantity = purchase_rack_drink_rack_drink_quantity,
                )
                
                purchase_rack_drink_rack_serializer = PurchaseRackDrinkRackSerializer(purchase_rack_drink_rack)
                
                return Response({'purchase_rack': purchase_rack_serializer.data, 'purchase_rack_drink_rack': purchase_rack_drink_rack_serializer.data, 'message': 'Casier de l\'achat enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
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
                
                purchase_rack_capacity = json_data.get('capacity')
                purchase_rack_quantity = json_data.get('quantity')
                purchase_rack_purchase_id = json_data.get('purchase')
                purchase_rack_purchase = Purchase.objects.get(id = purchase_rack_purchase_id)

                instance.capacity = purchase_rack_capacity
                instance.quantity = purchase_rack_quantity
                instance.purchase = purchase_rack_purchase
                instance.save()
                
                serializer = PurchaseRackSerializer(instance)
                
                return Response({'purchase_rack': serializer.data, 'message': 'Casier de l\'achat modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
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


# class PurchaseRackDrinkRackViewset(ModelViewSet):
    
#     serializer_class = PurchaseRackDrinkRackSerializer
    
#     def get_queryset(self):
#         queryset = PurchaseRackDrinkRack.objects.all()
        
#         return queryset
    
#     def create(self, request, *args, **kwargs):
#         # Vérifier si la méthode est POST et le contenu de la requête est JSON
#         if request.method == 'POST' and request.content_type == 'application/json':
#             try:
#                 json_data = request.data
                
#                 purchase_rack_drink_rack_purchase_rack = json_data.get('purchase_rack')
#                 purchase_rack_drink_rack_drink_rack = json_data.get('drink_rack')
#                 purchase_rack_drink_rack_drink_quantity = json_data.get('drink_quantity')
                
#                 purchase_rack_drink_rack = PurchaseRackDrinkRack.objects.create(
#                     purchase_rack = purchase_rack_drink_rack_purchase_rack,
#                     drink_rack = purchase_rack_drink_rack_drink_rack,
#                     drink_quantity = purchase_rack_drink_rack_drink_quantity,
#                 )
                
#                 serializer = PurchaseRackSerializer(purchase_rack_drink_rack)
                
#                 return Response({'purchase_rack_drink_rack': serializer.data, 'message': 'Capacité du casier enregistrée avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
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
                
#                 purchase_rack_drink_rack_purchase_rack = json_data.get('purchase_rack')
#                 purchase_rack_drink_rack_drink_rack = json_data.get('drink_rack')
#                 purchase_rack_drink_rack_drink_quantity = json_data.get('drink_quantity')

#                 instance.purchase_rack = purchase_rack_drink_rack_purchase_rack
#                 instance.drink_rack = purchase_rack_drink_rack_drink_rack
#                 instance.drink_quantity = purchase_rack_drink_rack_drink_quantity
#                 instance.save()
                
#                 serializer = PurchaseRackSerializer(instance)
                
#                 return Response({'purchase_rack_drink_rack': serializer.data, 'message': 'Capacité du casier modifiée avec succès.', 'type': success}, status=status.HTTP_200_OK)
#             except ValidationError as e:
#                 error_message = e.messages
                
#                 return Response({'message': error_message, 'type': error}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Si le contenu de la requête n'est pas JSON, renvoyer une erreur
#             return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)