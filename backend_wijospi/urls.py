from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from category.views import CategoryViewset
from packaging.views import PackagingViewset

router = routers.SimpleRouter()

router.register('category', CategoryViewset, basename='category')
router.register('packaging', PackagingViewset, basename='packaging')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
