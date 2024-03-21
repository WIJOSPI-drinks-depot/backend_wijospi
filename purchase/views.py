from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from purchase.models import Purchase
from purchase.serializers import PurchaseSerializer

# Messages types
error = 'error'
success = 'success'

class PurchaseViewset(ModelViewSet):
    
    serializer_class = PurchaseSerializer
    
    def get_queryset(self):
        queryset = Purchase.objects.filter(deleted_at = None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                purchase_date_time = json_data.get('date_time')
                purchase_customer = json_data.get('customer')
                purchase_storehouse = json_data.get('storehouse')
                
                purchase = Purchase.objects.create(
                    date_time = purchase_date_time,
                    customer = purchase_customer,
                    storehouse = purchase_storehouse,
                )
                
                serializer = PurchaseSerializer(purchase)
                
                return Response({'purchase': serializer.data, 'message': 'Achat enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
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
                
                purchase_date_time = json_data.get('date_time')
                purchase_customer = json_data.get('customer')
                purchase_storehouse = json_data.get('storehouse')
                
                instance.date_time = purchase_date_time
                instance.customer = purchase_customer
                instance.storehouse = purchase_storehouse
                instance.save()
                
                serializer = PurchaseSerializer(instance)
                
                return Response({'purchase': serializer.data, 'message': 'Achat modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
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
