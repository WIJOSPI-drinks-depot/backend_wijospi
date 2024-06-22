from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from category.views import CategoryViewset
# from storehouse.views import StorehouseDrinkRackViewset # Si on veut ajouter plusieurs boissons à un même approvisionnement
from customer.views import CustomerViewset
from drink_rack.views import DrinkRackViewset
from forecasting.views import GlabalForcastingViewSet
from packaging.views import PackagingViewset
from purchase.views import PurchaseViewset
from purchase_rack.views import PurchaseRackViewset
from purchase_rack.views import PurchaseRackDrinkRackViewset
from storehouse.views import StorehouseViewset
from supply.views import SupplyViewset

router = routers.SimpleRouter()

router.register('category', CategoryViewset, basename='category')
router.register('packaging', PackagingViewset, basename='packaging')
router.register('storehouse', StorehouseViewset, basename='storehouse')
# router.register('stock', StorehouseDrinkRackViewset, basename='stock') # Si on veut ajouter plusieurs boissons à un même approvisionnement
router.register('customer', CustomerViewset, basename='customer')
router.register('drink-rack', DrinkRackViewset, basename='drink-rack')
router.register('supply', SupplyViewset, basename='supply')
router.register('purchase', PurchaseViewset, basename='purchase')
router.register('purchase-rack', PurchaseRackViewset, basename='purchase-rack')
router.register('purchase-rack-drink-rack', PurchaseRackDrinkRackViewset, basename='purchase-rack-drink-rack')
# router.register('global-forecasting', GlabalForcastingViewSet, basename='global-forecasting')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/global-forecasting/', GlabalForcastingViewSet.as_view({'get': 'generation_global_forecasting'}), name='global-forecasting'),
    path('api/product-forecasting/<int:id>/', GlabalForcastingViewSet.as_view({'get': 'generation_product_forecasting'}), name='generation-product-forecasting'),
]
