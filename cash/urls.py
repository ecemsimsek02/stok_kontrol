from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CashRegisterViewSet, TransactionViewSet, ExpenseViewSet, CashRegisterRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'cash_registers', CashRegisterViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cash_registers/<int:pk>/', CashRegisterRetrieveUpdateDestroyView.as_view(), name='cashregister-detail'),
]
