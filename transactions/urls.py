from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleTransactionViewSet, PurchaseTransactionViewSet

router = DefaultRouter()
router.register(r'sale-transactions', SaleTransactionViewSet, basename='sale-transactions')
router.register(r'purchase-transactions', PurchaseTransactionViewSet, basename='purchase-transactions')


urlpatterns = [
    path('', include(router.urls)),
]
