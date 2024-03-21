from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customer.models import Customer
from customer.serializers import CustomerSerializer

# Messages types
error = 'error'
success = 'success'

class CustomerViewset(ModelViewSet):
    
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.filter(deleted_at = None)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Vérifier si la méthode est POST et le contenu de la requête est JSON
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                json_data = request.data
                
                customer_name = json_data.get('name')
                customer_surname = json_data.get('surname')
                customer_contact = json_data.get('contact')
                customer_address = json_data.get('address')
                customer_email = json_data.get('email')
                customer_hashed_password = make_password(json_data.get('password'))
                
                customer = Customer.objects.create(
                    name = customer_name,
                    surname = customer_surname,
                    contact = customer_contact,
                    address = customer_address,
                    email = customer_email,
                    password = customer_hashed_password,
                )
                
                serializer = CustomerSerializer(customer)
                
                return Response({'customer': serializer.data, 'message': 'Client enregistré avec succès.', 'type': success}, status=status.HTTP_201_CREATED)
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
                
                customer_name = json_data.get('name')
                customer_surname = json_data.get('surname')
                customer_contact = json_data.get('contact')
                customer_address = json_data.get('address')
                customer_email = json_data.get('email')
                customer_hashed_password = make_password(json_data.get('password'))
                
                instance.name = customer_name
                instance.surname = customer_surname
                instance.contact = customer_contact
                instance.address = customer_address
                instance.email = customer_email
                instance.password = customer_hashed_password
                instance.save()
                
                serializer = CustomerSerializer(instance)
                
                return Response({'customer': serializer.data, 'message': 'Client modifié avec succès.', 'type': success}, status=status.HTTP_200_OK)
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