from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from category.views import CategoryViewset

router = routers.SimpleRouter()

router.register('category', CategoryViewset, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
