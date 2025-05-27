from django.urls import path
from .views import (
    InvoiceListView,
    InvoiceDetailView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    invoice_detail_pdf
)

urlpatterns = [
    path('invoices-list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices-detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('update/<int:pk>/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('api/invoices/<int:pk>/pdf/', invoice_detail_pdf, name='invoice-pdf'),
]

from rest_framework.routers import DefaultRouter
from .api_views import InvoiceViewSet
from .views import invoice_detail_pdf
from django.urls import path, include

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('pdf/<int:pk>/', invoice_detail_pdf, name='invoice_detail_pdf'), 
]