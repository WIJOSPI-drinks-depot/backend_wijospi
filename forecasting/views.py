from django.db.models import F
from django.db.models.functions import TruncDate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from prophet import Prophet
import pandas as pd

from drink_rack.models import DrinkRack
from forecasting.serializers import PurchaseDataSerializer
from purchase.models import Purchase
from purchase_rack.models import PurchaseRack
from purchase_rack.models import PurchaseRackDrinkRack

class GlabalForcastingViewSet(ModelViewSet):

    serializer_class = PurchaseDataSerializer

    def get_queryset(self):
        queryset = PurchaseRackDrinkRack.objects.select_related(
            'drink_rack', 'purchase_rack__purchase'
        ).values(
            'drink_rack__name', 'drink_quantity', 'purchase_rack__purchase__date_time'
        )

        return queryset

    # Action personnalisée pour générer les prévisions de ventes
    def generation_global_forecasting(self, request):
        try:
            if request.method == 'GET':
                # Récupérez les données de ventes depuis la base de données
                sales_data = PurchaseRackDrinkRack.objects.select_related(
                    'drink_rack', 'purchase_rack__purchase'
                ).annotate(
                    ds=TruncDate('purchase_rack__purchase__date_time'),
                    y=F('drink_quantity')
                ).values(
                    'ds', 'y'
                )

                # return Response(sales_data)

                # Créez un DataFrame Pandas à partir des données de ventes
                df = pd.DataFrame(list(sales_data), columns=['ds', 'y'])

                # Convertir le champ date-heure en objets datetime pandas
                df['ds'] = pd.to_datetime(df['ds'])

                # Initialisez et ajustez le modèle Prophet
                model = Prophet()
                model.fit(df)

                # Générez des prévisions de ventes futures
                future_dates = model.make_future_dataframe(periods=30, freq='D', include_history=False)  # Par exemple, 30 jours de prévisions
                forecast = model.predict(future_dates)
                # forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

                # Convertissez les résultats de prévision en JSON pour passer en réponse
                forecast_json = forecast.to_json(orient='records')

                # Retournez les prévisions de ventes générées en réponse
                return Response({'forecast': forecast_json})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    # Action personnalisée pour générer les prévisions de ventes pour un produit spécifique
    # def generation_product_forecasting(self, request, id):
    #     try:
    #         if request.method == 'GET':
    #             # Récupérez les données de ventes depuis la base de données
    #             sales_data = PurchaseRackDrinkRack.objects.select_related(
    #                 'drink_rack', 'purchase_rack__purchase'
    #             ).annotate(
    #                 ds=TruncDate('purchase_rack__purchase__date_time'),
    #                 y=F('drink_quantity')
    #             ).values(
    #                 'drink_rack__name', 'ds', 'y'
    #             )

    #             # return Response(sales_data)

    #             # Créez un DataFrame Pandas à partir des données de ventes
    #             df = pd.DataFrame(list(sales_data), columns=['drink_rack__name', 'ds', 'y'])

    #             # Convertir le champ date-heure en objets datetime pandas
    #             df['ds'] = pd.to_datetime(df['ds'])

    #             # Initialisez et ajustez le modèle Prophet
    #             model = Prophet()
    #             model.fit(df)

    #             # Générez des prévisions de ventes futures
    #             future_dates = model.make_future_dataframe(periods=1, freq='D', include_history=False)  # Par exemple, 30 jours de prévisions
    #             forecast = model.predict(future_dates)
    #             forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    #             # Convertissez les résultats de prévision en JSON pour passer en réponse
    #             forecast_json = forecast.to_json(orient='records')
                
    #             # Ajouter les noms des produits aux prévisions de ventes générées
    #             for entry in forecast_json:
    #                 entry['drink_rack__name'] = id

    #             # Retournez les prévisions de ventes générées en réponse
    #             return Response({'forecast': forecast_json})
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    # def generation_product_forecasting(self, request, id):
    #     try:
    #         if request.method == 'GET':
    #             # Retrieve sales data from the database
    #             sales_data = PurchaseRackDrinkRack.objects.select_related(
    #                 'drink_rack', 'purchase_rack__purchase'
    #             ).annotate(
    #                 ds=TruncDate('purchase_rack__purchase__date_time'),
    #                 y=F('drink_quantity')
    #             ).values(
    #                 'drink_rack__name', 'ds', 'y'
    #             )

    #             # Create a Pandas DataFrame from the sales data
    #             df = pd.DataFrame(list(sales_data), columns=['drink_rack__name', 'ds', 'y'])

    #             # Check if DataFrame is empty
    #             if df.empty:
    #                 return Response({'error': 'No sales data available'}, status=status.HTTP_404_NOT_FOUND)

    #             # Convert the datetime field to pandas datetime objects
    #             df['ds'] = pd.to_datetime(df['ds'])

    #             # Get unique drink rack names
    #             drink_rack_names = df['drink_rack__name'].unique()

    #             # Initialize the result dictionary
    #             result = {}

    #             # Forecast sales for each drink rack
    #             for drink_rack_name in drink_rack_names:
    #                 df_filtered = df[df['drink_rack__name'] == drink_rack_name]

    #                 # Initialize and fit the Prophet model
    #                 model = Prophet()
    #                 model.fit(df_filtered[['ds', 'y']])

    #                 # Generate future sales predictions
    #                 future_dates = model.make_future_dataframe(periods=30, freq='D', include_history=False)  # Example: 30 days forecast
    #                 forecast = model.predict(future_dates)

    #                 # Convert forecast results to dictionary
    #                 forecast_dict = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')

    #                 # Include drink rack name in the forecast results
    #                 for entry in forecast_dict:
    #                     entry['drink_rack__name'] = drink_rack_name

    #                 # Add the forecast to the result dictionary
    #                 result[drink_rack_name] = forecast_dict

    #             # Return the generated sales forecasts for all drink racks
    #             return Response(result)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def generation_product_forecasting(self, request, id):
        drink_rack_name = DrinkRack.objects.get(id=id).name
        
        if(drink_rack_name) :
            try:
                if request.method == 'GET':
                    # Retrieve sales data from the database
                    sales_data = PurchaseRackDrinkRack.objects.select_related(
                        'drink_rack', 'purchase_rack__purchase'
                    ).annotate(
                        ds=TruncDate('purchase_rack__purchase__date_time'),
                        y=F('drink_quantity')
                    ).values(
                        'drink_rack__name', 'ds', 'y'
                    )

                    # Create a Pandas DataFrame from the sales data
                    df = pd.DataFrame(list(sales_data), columns=['drink_rack__name', 'ds', 'y'])

                    # Check if DataFrame is empty
                    if df.empty:
                        return Response({'error': 'No sales data available'}, status=status.HTTP_404_NOT_FOUND)

                    # Convert the datetime field to pandas datetime objects
                    df['ds'] = pd.to_datetime(df['ds'])

                    # Filter the DataFrame for the specific product (drink rack)
                    df_filtered = df[df['drink_rack__name'] == drink_rack_name]

                    if df_filtered.empty:
                        return Response({'error': f'No sales data available for the specified product ID: {id}'}, status=status.HTTP_404_NOT_FOUND)

                    # Initialize and fit the Prophet model
                    model = Prophet()
                    model.fit(df_filtered[['ds', 'y']])

                    # Generate future sales predictions
                    future_dates = model.make_future_dataframe(periods=30, freq='D', include_history=False)  # Example: 30 days forecast
                    forecast = model.predict(future_dates)

                    # Convert forecast results to JSON
                    forecast_json = forecast.to_dict(orient='records')

                    # Include drink rack name in the forecast results
                    for entry in forecast_json:
                        entry['drink_rack__name'] = drink_rack_name

                    # Return the generated sales forecast in the response
                    return Response({'forecast': forecast_json})

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)