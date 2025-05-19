# Standard library imports
import json
import logging

# Django core imports
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db import transaction

# Class-based views
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Third-party packages
from openpyxl import Workbook

# Local app imports
from store.models import Item
from accounts.models import Customer
from .models import Sale, Purchase
from .forms import PurchaseForm
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Sale, Purchase
from .serializers import SaleTransactionSerializer, PurchaseTransactionSerializer

class SaleTransactionViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related('invoice').all().order_by('-invoice__date')
    serializer_class = SaleTransactionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delivery_status = request.data.get('delivery_status', instance.delivery_status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PurchaseTransactionViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.select_related('bill').all().order_by('-bill__date')
    serializer_class = PurchaseTransactionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delivery_status = request.data.get('delivery_status', instance.delivery_status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)