"""
from django.urls import path
from .views import CategoryViewSet, ItemViewSet, DeliveryViewSet

urlpatterns = [
    path("category/", CategoryViewSet.as_view(), name="dashboard"),
    path("items/", ItemViewSet.as_view(), name="item-list"),
    path("delivery/", DeliveryViewSet.as_view(), name="item-search"),
 
]
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ItemViewSet, DeliveryViewSet

# API router'ını oluşturuyoruz
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Router'ı URL'lere dahil ediyoruz
]

