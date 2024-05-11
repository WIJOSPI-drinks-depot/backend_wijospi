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
                forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

                # Convertissez les résultats de prévision en JSON pour passer en réponse
                forecast_json = forecast.to_json(orient='records')

                # Retournez les prévisions de ventes générées en réponse
                return Response({'forecast': forecast_json})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)