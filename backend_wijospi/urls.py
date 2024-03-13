from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from category.views import CategoryViewset
from packaging.views import PackagingViewset
from storehouse.views import StorehouseViewset
from customer.views import CustomerViewset

router = routers.SimpleRouter()

router.register('category', CategoryViewset, basename='category')
router.register('packaging', PackagingViewset, basename='packaging')
router.register('storehouse', StorehouseViewset, basename='storehouse')
router.register('customer', CustomerViewset, basename='customer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
